from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
import torch
import os
import sys
import django
from torch.utils.data import DataLoader
from sklearn.utils.class_weight import compute_class_weight

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentAnalysis.settings')
django.setup()
from WebApplication.models import Data

# Step 1: Prepare the dataset
def prepare_data():
    """Load and split data into training and validation sets."""
    dataset = Data.objects.values('comment_body_corrected', 'comment_labels')

    texts = [entry['comment_body_corrected'] for entry in dataset]
    labels = [entry['comment_labels'] for entry in dataset]

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    return train_texts, val_texts, train_labels, val_labels


# Step 2: Tokenize the data
def tokenize_data(tokenizer, texts, labels, max_length=128):
    """Tokenize text data and create a dataset."""
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length)
    dataset = SentimentDataset(encodings, labels)
    return dataset


class SentimentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item


# Step 3: Define training function using Trainer
def train_with_trainer():
    """Train and evaluate the model using Trainer."""
    # Prepare data
    train_texts, val_texts, train_labels, val_labels = prepare_data()

    # Initialize tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

    # Tokenize and create datasets
    train_dataset = tokenize_data(tokenizer, train_texts, train_labels)
    val_dataset = tokenize_data(tokenizer, val_texts, val_labels)

    # Compute class weights to handle imbalance
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_labels),
        y=train_labels
    )
    class_weights = torch.tensor(class_weights).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    # Override model's loss function with weighted loss
    def custom_loss(model, inputs):
        labels = inputs.pop('labels')
        outputs = model(**inputs)
        logits = outputs.logits
        loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights)
        loss = loss_fn(logits, labels)
        return loss, outputs

    model.compute_loss = custom_loss  # Replace default loss function

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=5,  # Experiment with longer training
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir='./logs',
        logging_steps=10,
        learning_rate=5e-5,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        gradient_accumulation_steps=2,  # Accumulate gradients for larger effective batch size
        fp16=torch.cuda.is_available(),  # Use mixed precision if supported
        gradient_checkpointing=True  # Reduce memory usage
    )

    # Define the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    # Train and evaluate
    trainer.train()
    trainer.save_model("sentiment_model2")
    tokenizer.save_pretrained("sentiment_model2")
    print("Model and tokenizer saved to 'sentiment_model2'.")


# Step 4: Define custom metric function
def compute_metrics(eval_pred):
    """Compute accuracy, precision, recall, and F1 score."""
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='binary')
    acc = accuracy_score(labels, predictions)
    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


# Debugging: Inspect gradient flow and logits
class GradientDebugger:
    @staticmethod
    def inspect_gradients(model):
        for name, param in model.named_parameters():
            if param.requires_grad and param.grad is not None:
                print(f"{name}: Gradient norm {param.grad.norm().item()}.")

    @staticmethod
    def inspect_logits(logits):
        print(f"Logits: {logits}")


# Main execution
if __name__ == "__main__":
    train_with_trainer()
