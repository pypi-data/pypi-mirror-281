import numpy as np

class PyTulpa:
    def __init__(self):
        self.model = None
        self.optimizer = None
        self.loss_fn = None

    def compile(self, model, optimizer, loss_fn):
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn

    def train(self, X, y, epochs=100, batch_size=32, validation_data=None):
        history = {'train_loss': [], 'val_loss': []}
        
        for epoch in range(epochs):
            epoch_loss = 0
            for i in range(0, len(X), batch_size):
                batch_X = X[i:i+batch_size]
                batch_y = y[i:i+batch_size]
                
                y_pred = self.model.forward(batch_X)
                loss = self.loss_fn(batch_y, y_pred)
                epoch_loss += loss
                
                gradients = self.model.backward(batch_y)
                self.optimizer.update(self.model.parameters(), gradients)
            
            avg_loss = epoch_loss / (len(X) // batch_size)
            history['train_loss'].append(avg_loss)
            
            if validation_data:
                val_X, val_y = validation_data
                val_pred = self.predict(val_X)
                val_loss = self.loss_fn(val_y, val_pred)
                history['val_loss'].append(val_loss)
                print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}, Val Loss: {val_loss:.4f}")
            else:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
        
        return history

    def predict(self, X):
        return self.model.forward(X)