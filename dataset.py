import os

folder = "ai_dataset"
os.makedirs(folder, exist_ok=True)

data = {
    "ai_intro.txt": "Artificial Intelligence is the simulation of human intelligence by machines. It includes learning, reasoning, and problem-solving.",
    "machine_learning.txt": "Machine Learning enables systems to learn from data and improve automatically without explicit programming.",
    "deep_learning.txt": "Deep Learning uses neural networks with many layers to model complex patterns in data.",
    "neural_networks.txt": "Neural networks are inspired by the human brain and consist of interconnected nodes.",
    "cnn.txt": "Convolutional Neural Networks are used mainly for image processing and computer vision tasks.",
    "rnn.txt": "Recurrent Neural Networks are used for sequential data like text and speech.",
    "lstm.txt": "LSTM is a type of RNN designed to remember long-term dependencies.",
    "gru.txt": "GRU is a simplified version of LSTM used in sequence modeling.",
    "nlp.txt": "Natural Language Processing enables machines to understand and process human language.",
    "computer_vision.txt": "Computer Vision allows machines to interpret and analyze visual data.",
    "reinforcement_learning.txt": "Reinforcement Learning trains agents using rewards and penalties.",
    "supervised_learning.txt": "Supervised learning uses labeled data for training models.",
    "unsupervised_learning.txt": "Unsupervised learning finds patterns in unlabeled data.",
    "semi_supervised_learning.txt": "Semi-supervised learning uses both labeled and unlabeled data.",
    "transfer_learning.txt": "Transfer learning reuses pre-trained models for new tasks.",
    "feature_engineering.txt": "Feature engineering improves model performance by selecting relevant features.",
    "data_preprocessing.txt": "Data preprocessing involves cleaning and transforming raw data.",
    "model_evaluation.txt": "Model evaluation measures performance using metrics like accuracy and precision.",
    "overfitting.txt": "Overfitting occurs when a model learns noise instead of patterns.",
    "underfitting.txt": "Underfitting occurs when a model fails to capture patterns.",
    "bias_variance.txt": "Bias-variance tradeoff balances model complexity and accuracy.",
    "gradient_descent.txt": "Gradient descent is used to minimize loss functions in ML models.",
    "backpropagation.txt": "Backpropagation updates weights in neural networks.",
    "activation_functions.txt": "Activation functions introduce non-linearity in neural networks.",
    "decision_trees.txt": "Decision trees split data into branches for decision making.",
    "random_forest.txt": "Random forest is an ensemble of multiple decision trees.",
    "support_vector_machine.txt": "SVM is used for classification by finding optimal hyperplanes.",
    "k_means_clustering.txt": "K-means groups data into clusters based on similarity.",
    "dimensionality_reduction.txt": "Dimensionality reduction reduces features while preserving information.",
    "ai_ethics.txt": "AI ethics focuses on fairness, transparency, and accountability in AI systems."
}

for filename, content in data.items():
    with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Dataset created successfully!")