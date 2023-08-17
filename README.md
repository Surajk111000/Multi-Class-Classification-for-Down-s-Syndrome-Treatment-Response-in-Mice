# Multi-Class-Classification-for-Down-s-Syndrome-Treatment-Response-in-Mice
This code addresses the challenge of training successful classification models for a specific biological problem involving mice experiments related to Down's syndrome treatment assessment. The code starts by reading data directly from an online source. It conducts exploratory data analysis to determine usable variables, correlations, and class balance. Missing variable handling is performed using multivariate feature imputation. Appropriate metrics, such as accuracy, F1 score, balanced accuracy, and AUC, are chosen for the two separate classification tasks: binary and multi-class. The code then employs five-fold cross-validation to optimize hyperparameters for various models, including linear SVM, RBF kernel SVM, neural network, and random forest. Feature importance analysis is conducted to identify significant proteins for each model. Systematic feature elimination is considered to enhance models. Promising models are tested on test data. Additionally, a pre-trained ConvNet is used to extract features, followed by comparisons among L2 regularized logistic regression, SVM, and random forest models, evaluated on test data for accuracy and F1 score. The findings are summarized, and references are provided.

References:
[0] Source: https://www.ee.iitb.ac.in/~asethi/Dump/MouseTrain.csv
[1] Multivariate Feature Imputation: https://scikit-learn.org/stable/modules/impute.html
[2] PyTorch Transfer Learning Tutorial: https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
[3] Scikit-learn for Model Selection and Evaluation: https://scikit-learn.org/stable/modules/grid_search.html

Highlight of code
•	Analysed data, mitigated correlations, and imputed values for improved classification.
•	Optimized SVM, Neural Network, and Random Forests hyperparameters through validation. 
•	Improved model efficiency by assessing feature significance and refining variables.
