import torch
import mlflow
import matplotlib.pyplot as plt
import pandas as pd
import torch.nn as nn
from datasets import Dataset
from transformers import (
    Trainer, TrainingArguments, RobertaTokenizerFast,
    EarlyStoppingCallback, BertTokenizer
)
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from torch.utils.data import DataLoader, TensorDataset
from typing import Tuple, Dict, Any
from emotion_detective.logger.logger import setup_logging
from azureml.core import Run

logger = setup_logging()

def train_and_evaluate_roberta(
    roberta_model: nn.Module,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    output_dir: str = './',
    logging_dir: str = './',
    num_train_epochs: int = 1,
    train_batch_size: int = 4,
    eval_batch_size: int = 8,
    gradient_accumulation_steps: int = 16,
    learning_rate: float = 2e-5,
    warmup_steps: int = 500,
    weight_decay: float = 0.01,
    logging_steps: int = 8,
    disable_tqdm: bool = False,
    dataloader_num_workers: int = 8,
    seed: int = 42,
    early_stopping_patience: int = 3,
    cloud_logging: bool = False
) -> Tuple[nn.Module, Dict[str, Any]]:
    """
    Train and evaluate a RoBERTa model using the given training and test data.

    Args:
        roberta_model: Pre-trained RoBERTa model to fine-tune.
        train_data: Training data in a pandas DataFrame.
        test_data: Test data in a pandas DataFrame.
        output_dir: Directory to save the model and outputs.
        logging_dir: Directory to save the logs.
        num_train_epochs: Number of training epochs.
        train_batch_size: Batch size for training.
        eval_batch_size: Batch size for evaluation.
        gradient_accumulation_steps: Number of gradient accumulation steps.
        learning_rate: Learning rate for training.
        warmup_steps: Number of warmup steps.
        weight_decay: Weight decay for the optimizer.
        logging_steps: Frequency of logging.
        disable_tqdm: Disable tqdm progress bar if "True".
        dataloader_num_workers: Number of worker threads for data loading.
        seed: Random seed for reproducibility.
        early_stopping_patience: Patience for early stopping.
        cloud_logging: Enable cloud logging with MLflow if True.

    Returns:
        A tuple containing the trained model and evaluation results.

    Author: Rebecca Borski
    """
    
    # Load tokenizer
    logger.info("Loading tokenizer...")
    tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base', max_length=512)

    def tokenization(batched_text: Dict[str, Any]) -> Dict[str, Any]:
        return tokenizer(batched_text['text'], padding=True, truncation=True)

    # Map the tokenization function to your DataFrame
    logger.info("Tokenizing data...")
    tokenized_train_data = Dataset.from_pandas(train_data).map(
        tokenization, batched=True, batch_size=len(train_data)
    )
    tokenized_test_data = Dataset.from_pandas(test_data).map(
        tokenization, batched=True, batch_size=len(test_data)
    )
    logger.info("Tokenization complete.")
    
    tokenized_train_data.set_format('torch',
                                    columns=['input_ids', 'attention_mask', 'label'])
    tokenized_test_data.set_format('torch',
                                   columns=['input_ids', 'attention_mask', 'label'])

    # Define compute_metrics function
    logger.info("Defining compute_metrics function...")
    def compute_metrics(pred: Any) -> Dict[str, float]:
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels,
                                                                   preds,
                                                                   average='micro')
        acc = accuracy_score(labels, preds)
        return {
            'accuracy': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }
    logger.info("compute_metrics function defined.")

    # Define the TrainingArguments
    logger.info("Defining TrainingArguments...")
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir=logging_dir,
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=eval_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        num_train_epochs=num_train_epochs,
        logging_steps=logging_steps,
        learning_rate=learning_rate,
        warmup_steps=warmup_steps,
        weight_decay=weight_decay,
        disable_tqdm=disable_tqdm,
        dataloader_num_workers=dataloader_num_workers,
        seed=seed,
        report_to=[],  # Disable wandb and other logging services
        load_best_model_at_end=True,
        metric_for_best_model='eval_loss',
    )
    logger.info("TrainingArguments defined.")
    
    # Instantiate Trainer with EarlyStoppingCallback
    logger.info("Instantiating Trainer...")
    trainer = Trainer(
        model=roberta_model,
        args=training_args,
        train_dataset=tokenized_train_data,
        eval_dataset=tokenized_test_data,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(
            early_stopping_patience=early_stopping_patience
            )]
    )
    logger.info("Trainer instantiated.")

    if cloud_logging:
        mlflow.start_run()
        logger.info("MLflow run started.")

    # Start training
    logger.info("Training model...")
    trainer.train()

    # Evaluate the model
    logger.info("Evaluating model...")
    eval_results = trainer.evaluate()

    if cloud_logging:
        for key, value in eval_results.items():
            mlflow.log_metric(key, value)
        mlflow.end_run()

    # Return the trained model and evaluation results
    return trainer.model, eval_results

def train_and_evaluate_rnn(
    model: nn.Module,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    num_epochs: int = 3,
    early_stopping_patience: int = 3,
    learning_rate: float = 0.001,
    train_batch_size: int = 4,
    eval_batch_size: int = 8,
    cloud_logging: bool = False
) -> nn.Module:
    """
    Train and evaluate an RNN model using the given training and test data.

    Args:
        model: RNN model to train.
        train_data: Training data in a pandas DataFrame.
        test_data: Test data in a pandas DataFrame.
        num_epochs: Number of training epochs.
        early_stopping_patience: Patience for early stopping.
        learning_rate: Learning rate for training.
        train_batch_size: Batch size for training.
        eval_batch_size: Batch size for evaluation.
        cloud_logging: Enable cloud logging with MLflow if True.

    Returns:
        The trained RNN model.

    Author: Rebecca Borski
    """
    run = Run.get_context()

    logger.info("Initializing tokenizer")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    logger.info("Tokenizing data")
    def tokenize(text: str, tokenizer: BertTokenizer, max_len: int = 512) -> torch.Tensor:
        return tokenizer.encode(text, max_length=max_len, truncation=True, padding='max_length')

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    logger.info("Creating DataLoader objects")
    train_data['input_ids'] = train_data['text'].apply(lambda x: tokenize(x, tokenizer))
    test_data['input_ids'] = test_data['text'].apply(lambda x: tokenize(x, tokenizer))

    logger.info("Creating TensorDataset objects")
    train_dataset = TensorDataset(
        torch.tensor(train_data['input_ids'].tolist()),
        torch.tensor(train_data['label'].tolist())
    )
    test_dataset = TensorDataset(
        torch.tensor(test_data['input_ids'].tolist()),
        torch.tensor(test_data['label'].tolist())
    )

    logger.info("Creating DataLoader objects")
    train_loader = DataLoader(train_dataset, batch_size=train_batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=eval_batch_size, shuffle=False)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    best_val_loss = float('inf')
    patience_counter = 0
    best_model = None

    if cloud_logging:
        logger.info("Starting MLflow run")
        mlflow.start_run()

    logger.info("Training model")
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        logger.info(f"Epoch {epoch + 1}/{num_epochs}")
        for input_ids, labels in train_loader:
            input_ids, labels = input_ids.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(input_ids)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        logger.info('Setting model to evaluation mode')
        model.eval()
        eval_loss = 0
        all_preds = []
        all_labels = []
        with torch.no_grad():
            for input_ids, labels in test_loader:
                input_ids, labels = input_ids.to(device), labels.to(device)
                outputs = model(input_ids)
                loss = criterion(outputs, labels)
                eval_loss += loss.item()
                preds = torch.argmax(outputs, dim=1)
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

        logger.info('Calculating metrics')
        train_loss = total_loss / len(train_loader)
        eval_loss /= len(test_loader)

        precision, recall, f1, _ = precision_recall_fscore_support(
            all_labels, all_preds, average='weighted', zero_division=1
        )
        accuracy = accuracy_score(all_labels, all_preds)

        print(f'Epoch {epoch + 1}/{num_epochs}')
        print(f'Train Loss: {train_loss:.4f}')
        print(f'Val Loss: {eval_loss:.4f}, Accuracy: {accuracy:.4f}',
              f'Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}')

        if cloud_logging:
            run.log("train_loss", train_loss)
            run.log("eval_loss", eval_loss)
            run.log("accuracy", accuracy)
            run.log("precision", precision)
            run.log("recall", recall)
            run.log("f1_score", f1)

        # Implementing early stopping
        if eval_loss < best_val_loss:
            best_val_loss = eval_loss
            best_model = model
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= early_stopping_patience:
                print(f'Early stopping at epoch {epoch + 1}',
                      f'with best validation loss: {best_val_loss:.4f}')
                if cloud_logging:
                    run.complete()
                return best_model

    if cloud_logging:
        # Plot the training and validation loss and accuracies
        # for each epoch using matplotlib and log the image to Azure ML
        plt.figure()
        plt.plot(range(num_epochs), train_loss, label='train_loss')
        plt.plot(range(num_epochs), eval_loss, label='val_loss')
        plt.plot(range(num_epochs), accuracy, label='accuracy')
        plt.plot(range(num_epochs), precision, label='precision')
        plt.plot(range(num_epochs), recall, label='recall')
        plt.title("Learning curves")
        plt.xlabel("Epochs")
        plt.ylabel("Metrics")
        plt.legend(loc="lower left")
        plt.savefig("learning_metrics.png")
        run.log_image("Learning curves", path="learning_metrics.png")
        run.complete()

    return model
