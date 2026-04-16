from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load model
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

# Training data
data = [
("Convert to SQL: show all students", "SELECT * FROM students;"),
("Convert to SQL: students with marks above 80", "SELECT * FROM students WHERE marks > 80;"),
("Convert to SQL: students with marks above 70", "SELECT * FROM students WHERE marks > 70;"),
("Convert to SQL: students with marks below 50", "SELECT * FROM students WHERE marks < 50;"),
("Convert to SQL: students with marks below 30", "SELECT * FROM students WHERE marks < 30;"),
("Convert to SQL: students in chennai", "SELECT * FROM students WHERE city = 'Chennai';"),
("Convert to SQL: students in mumbai", "SELECT * FROM students WHERE city = 'Mumbai';"),
("Convert to SQL: students in delhi", "SELECT * FROM students WHERE city = 'Delhi';"),
("Convert to SQL: students in chennai with marks above 80", "SELECT * FROM students WHERE city = 'Chennai' AND marks > 80;"),
("Convert to SQL: students in mumbai with marks below 50", "SELECT * FROM students WHERE city = 'Mumbai' AND marks < 50;"),
("Convert to SQL: count students", "SELECT COUNT(*) FROM students;"),
("Convert to SQL: count students in chennai", "SELECT COUNT(*) FROM students WHERE city = 'Chennai';"),
("Convert to SQL: top 3 students", "SELECT * FROM students ORDER BY marks DESC LIMIT 3;"),
("Convert to SQL: top 5 students", "SELECT * FROM students ORDER BY marks DESC LIMIT 5;"),
]
# Optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# Training loop
model.train()

for epoch in range(5):  # keep small (fast training)
    print(f"Epoch {epoch+1}")

    for inp, out in data:
        inputs = tokenizer(inp, return_tensors="pt", padding=True, truncation=True)
        labels = tokenizer(out, return_tensors="pt", padding=True, truncation=True).input_ids

        outputs = model(**inputs, labels=labels)
        loss = outputs.loss

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        print("Loss:", loss.item())

# Save model
model.save_pretrained("./model")
tokenizer.save_pretrained("./model")

print("✅ Training completed and model saved!")