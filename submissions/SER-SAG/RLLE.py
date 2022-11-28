# Author: Isidora Jankov

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.multivariate.pca import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.manifold import LocallyLinearEmbedding, Isomap
from scipy.stats import zscore

import wpca # https://github.com/jakevdp/wpca


def RobustPCA(hood, sample, d_out=3):
    
    """
    Chang & Yeung (2006) - steps from section 4.3 Robust PCA. The code calculates the reliability score
    of one data point from its neighborhood.
    
    Parameters:
    -----------
    hood: pd.DataFrame
        Neighborhood of the given point.
    sample: pd.DataFrame
        Data from which the given points was sampled.
        
    Returns:
    --------
    a: float
        Reliability score of the input data point.
    """
    
    # Normalization of a given neighbourhood
    norm_hood = hood.apply(zscore)
        
    hood = hood.T
    norm_hood = norm_hood.T
    
    #print('Neighbourhood dimension (D x k): {} x {}'.format(hood.shape[0], hood.shape[1]))
    #print('Sample dimension (N x D): {} x {}'.format(sample.shape[0], sample.shape[1]))
    
    N = sample.shape[0] # number of points in the sample
    D = sample.shape[1] # number of features i.e. original dimensionality
    k = hood.shape[1]   # number of neighbors
    
    # Evaluating d_init and B_init
    d_init = np.zeros((D,1)) # for standardized data, mean vector is zero vector.
    #print('d_init dimension (D x 1): {} x {}'.format(d_init.shape[0], d_init.shape[1]))
    
    pca = PCA(hood.T, ncomp=d_out, standardize=True) # regular PCA

    B_init = pca.eigenvecs # get eigenvectors
    #print('B_init dimension (D x d): {} x {} \n'.format(B_init.shape[0], B_init.shape[1]))
    
    # Define 2D and 3D arrays for storing all mean vectors d and eigenvector sets B (for each iteration)
    d_matrix = np.empty([D,50])
    B_matrix = np.empty([D,d_out,50])
    d_matrix[:,0] = d_init.flatten() # store mean vector from 0th iteration
    B_matrix[:,:,0] = B_init # store eigenvector matrix for 0th iteration
    
    # Set initial value for deltas
    delta_d = 5
    delta_B = 5  
    
    
    # Iteratively reweighted PCA (as described in Chang & Yeung 2006)
    
    i = 0
    
    while ((delta_d >= 0.0001) & (delta_B >= 0.0001) & (i < 49)):
        
        #print('d dimension from iteration {}: {} x {}'.format(i+1, d.shape[0], d.shape[1]))
        #print('B dimension from iteration {}: {} x {}'.format(i+1, B.shape[0], B.shape[1]))
        
        # Get d and B from previous iteration (i)
        d = d_matrix[:,i]
        d = d.reshape(D,1)
        B = B_matrix[:,:,i]
        
        #print('Iteration {}\n'.format(i+1))
        
        # Calculating error(e) --> dim: D x k
        delta = norm_hood - d
        e = delta - np.dot(np.dot(B, B.T), delta)
        e_norm = np.linalg.norm(e, d_out, axis=0)

        # Calculating weights(a) --> dim: k
        c = 0.5 * (1/k) * e_norm.sum()
        a = np.where(np.abs(e_norm) <= c, 1, c/np.abs(e_norm)) # evaluating weight function
        #print('Weights from previous iteration: \n', a,'\n')
        
        # Set same weights for each parameter (weights for individual parameters are not considered in this algorithm)
        a_matrix = np.empty((k, D))
        for dim in range(D):
            a_matrix[:,dim] = a
            
        # Calculating new d
        d = ((a * hood).sum(axis=1))/a.sum()
        d = d.values.reshape(D,1)
        d_matrix[:,i+1] = d.flatten() # storing result in matrix

        # Calculating B using weighted PCA
        pca = wpca.WPCA(n_components=d_out).fit(hood.T, weights=a_matrix)
        B = pca.components_.T
        B_matrix[:,:,i+1] = B # storing result in matrix
        #print('d:', d, '\n')
        #print('B:', B, '\n')
        
        # Calculating difference in d and B between iterations i and i+1
        delta_d = np.abs((d_matrix[:,i+1]-d_matrix[:,i])).sum()
        delta_B = np.abs((B_matrix[:,:,i+1]-B_matrix[:,:,i])).sum()
        #print('|Delta_d| = {} \n'.format(delta_d))
        #print('|Delta_B| = {} \n'.format(delta_B))
        #print('=========================================================')
        i = i+1

    return a

def RLLE_outliers(sample, k=15, outlier_ratio = 0.05, d_out=3, metric='minkowski', normalization='z-score'):
    
    """Perform outlier search and removal using reliability scores calculated from Robust PCA.
    Points with lower reliability score are more likely to be an outlier. Outliers have two general
    properties: first, they will not be members of large number of local neighborhoods; second,
    the neighborhoods in which they appear, they will be far from the best fit hyperplane. This
    code removes outliers with lowest scores based on user defined outlier ratio.
    
    Parameters:
    -----------
    sample: pd.DataFrame
        A dataframe where rows are individual measurments and columns are different parameters
        (features). Columns should be named.
    k: int, default=15
        Number of nearest neighbors.
    outlier_ratio: float, default=0.05
        Ratio of outliers in the sample
    d_out: int, default=3
        Number of output dimesnions in RobustPCA
    metric: str, default='minkowski', options: {'geodesic', 'mahalanobis', 'minkowski'}
        Metric for distance calculation in neighbor search. Default is 'minkowski' with arg p=2,
        which corresponds to Euclidian distance.
    normalization: str, default='z-score', options: {'z-score', 'min-max', False}
        Normalization method used before applying nearest neighbor search.
        
    Returns:
    --------
    new_sample: pd.DataFrame
        A sample without outliers.
    new_idx: pd.Series
        Indices of measurments which are not considered to be outliers.
    outliers: pd.DataFrame
        Outliers removed from the original sample.
    scores: np.array
        Reliability scores of all points from original sample.
    """
    
    start = time.time()
    
    # Ensure that index goes from 0 to n-1
    sample = sample.reset_index(drop=True)
    
    # Number of points
    N = sample.shape[0]
    
    # Number of outliers
    outlier_num = int(N * outlier_ratio)
    
    # Normalizing features (z-score)
    st_sample = sample.apply(zscore)
    
    # Normalizing features (min-max)
    scaler = MinMaxScaler()
    norm_sample = pd.DataFrame(scaler.fit_transform(sample), columns=sample.columns)
        
    if normalization == False:
        norm_sample = sample
    
    
    # Find k-neighbors for all data points
    
    if metric == "geodesic":
        # Geodesic distances obtained using IsoMap
        Y_isomap, err, G = compute_isomap(norm_sample, n_neighbors=15, out_dim=3)
        nbrs = NearestNeighbors(n_neighbors=k, algorithm='brute', metric="precomputed").fit(G)
        distances, indices = nbrs.kneighbors(G)
        
    elif metric == "mahalanobis":
        nbrs = NearestNeighbors(n_neighbors=k, algorithm='brute', metric='mahalanobis', 
                                metric_params={'V': np.cov(st_sample)}).fit(st_sample)
        distances, indices = nbrs.kneighbors(st_sample)
    else:
        if normalization == "z-score":
            nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree', metric=metric).fit(st_sample)
            distances, indices = nbrs.kneighbors(st_sample)
        elif normalization == "min-max":
            nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree', metric=metric).fit(norm_sample)
            distances, indices = nbrs.kneighbors(norm_sample)

    
    # Calculating reliability scores using RobustPCA (Chang & Yeung 2006)
    
    scores = np.zeros(N)
    for i in range(N):
        #print('Object index:', i)
        hood = sample.iloc[indices[i,:],:] # select k-neighbors for point x_i (matrix D x k, i=1,..,N)
        a = RobustPCA(hood, sample, d_out)
        a_norm = a/(a.sum())
        scores[indices[i,:]] = scores[indices[i,:]] + a_norm
    
    # Selecting and removing outliers (points with smallest scores)
    nsmall = pd.Series(scores).nsmallest(outlier_num)
    outliers = sample.iloc[nsmall.index,:]
    new_sample = sample.drop(index=outliers.index)
    idx = sample.index.to_series()
    new_idx = idx.drop(index=outliers.index)
    
    # Plot histogram of reliability scores
    plt.hist(scores, bins=20, color='c')
    plt.axvline(nsmall.max(), label='Outlier cutoff at {:.2f}'.format(nsmall.max()), c='red', linestyle='--')
    plt.axvline(np.median(scores), label='Median at {:.2f}'.format(np.median(scores)), c='blue', linestyle='--')
    plt.xlabel('Reliability score')
    plt.ylabel('Count')
    plt.legend()
    plt.show()
    
    print("Runtime: {:.2f} seconds".format(time.time()-start))
    
    return new_sample, new_idx, outliers, scores



def compute_LLE(data, n_neighbors=10, out_dim=3, method='modified'):
    """ Applies the Locally Linear Embedding algorithm from sci-kit learn on a given dataset and
    returns the coordinates in the projected space, as well as the reconstruction error.
    
    Parameters:
    -----------
    data: array-like of shape [n_samples, n_features]
        Data on which we want to run the alghoritm.
    n_neighbors: int
        Number of nearest neighbors to include in the calculation. Default is 10.
    out_dim: int
        Dimension of the projected space. Default is 3.
    method: string ('standard', 'hessian', 'modified' or 'ltsa')
        Different methods of calculating LLE. Default is 'modified'.
        
    Returns:
    --------
    Y_LLE: array-like of shape[n_samples, n_components]
        New dataframe/array containing the coordinates in the projected space.
    err: float
        Reconstruction error associated with the embedded vectors.
    """
    
    LLE = LocallyLinearEmbedding(n_neighbors=n_neighbors, n_components=out_dim, method=method, eigen_solver='dense')
    Y_LLE = LLE.fit_transform(data)
    #print (" - finished LLE projection")
    err = LLE.reconstruction_error_
    #print (" - reconstruction error: ", err)
    
    return Y_LLE, err



def compute_isomap(data, n_neighbors=10, out_dim=3):
    """ Applies the Isometric Mapping algorithm from sci-kit learn on a given dataset and
    returns the coordinates in the projected space, the reconstruction error and the matrix of
    pairwise geodesic distances.
    
    Parameters:
    -----------
    n_neighbors: int
        Number of nearest neighbors to include in the calculation. Default is 10.
    out_dim: int
        Dimension of the projected space. Default is 3.
    data: array-like of shape [n_samples, n_features]
        Data on which we want to apply (train) the alghoritm.
        
    Returns:
    --------
    Y_isomap: array-like of shape[n_samples, n_components]
        New dataframe/array containing the coordinates in the projected space.
    err: float
        Reconstruction error associated with the embedded vectors.
    G: array-like of shape [n_samples, n_samples]
        Stores the geodesic distance matrix of training data.
    """
    
    isomap = Isomap(n_neighbors=n_neighbors, n_components=out_dim, eigen_solver='dense')
    Y_isomap = isomap.fit_transform(data)
    #print (" - finished isomap projection")
    err = isomap.reconstruction_error()
    #print (" - reconstruction error: ", err)
    G = isomap.dist_matrix_

    return Y_isomap, err, G















