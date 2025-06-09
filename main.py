from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Split App")

# CORS for frontend/Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to the Split App Backend!"}

@app.post("/expenses")
def add_expense(amount: float, description: str, paid_by: str, db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if not description or not paid_by:
        raise HTTPException(status_code=400, detail="Missing fields")

    new_expense = models.Expense(amount=amount, description=description, paid_by=paid_by)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return {
        "success": True,
        "data": {
            "id": new_expense.id,
            "amount": new_expense.amount,
            "description": new_expense.description,
            "paid_by": new_expense.paid_by
        },
        "message": "Expense added successfully"
    }
@app.get("/expenses")
def list_expenses(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    return {
        "success": True,
        "data": [
            {
                "id": expense.id,
                "amount": expense.amount,
                "description": expense.description,
                "paid_by": expense.paid_by
            }
            for expense in expenses
        ]
    }
@app.get("/people")
def get_people(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    people_set = set(expense.paid_by.strip().title() for expense in expenses)
    return {
        "success": True,
        "people": list(people_set)
    }
@app.get("/settlements")
def get_settlements(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()

    # Calculate total paid per person
    person_totals = {}
    for expense in expenses:
        person = expense.paid_by.strip().title()
        person_totals[person] = person_totals.get(person, 0) + expense.amount

    people = list(person_totals.keys())
    total_spent = sum(person_totals.values())
    num_people = len(people)

    if num_people == 0:
        return {"success": True, "settlements": []}

    fair_share = total_spent / num_people

    # Compute balances
    balances = {
        person: round(person_totals[person] - fair_share, 2)
        for person in people
    }

    # Separate creditors and debtors
    debtors = []
    creditors = []

    for person, balance in balances.items():
        if balance < 0:
            debtors.append([person, -balance])
        elif balance > 0:
            creditors.append([person, balance])

    settlements = []

    # Greedy matching between debtors and creditors
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt = debtors[i]
        creditor, credit = creditors[j]
        settled_amount = min(debt, credit)
        settlements.append({
            "from": debtor,
            "to": creditor,
            "amount": round(settled_amount, 2)
        })

        debt -= settled_amount
        credit -= settled_amount

        if debt == 0:
            i += 1
        else:
            debtors[i][1] = debt

        if credit == 0:
            j += 1
        else:
            creditors[j][1] = credit

    return {"success": True, "settlements": settlements}
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, amount: float, description: str, paid_by: str, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.amount = amount
    expense.description = description
    expense.paid_by = paid_by
    db.commit()
    db.refresh(expense)

    return {
        "success": True,
        "data": {
            "id": expense.id,
            "amount": expense.amount,
            "description": expense.description,
            "paid_by": expense.paid_by
        },
        "message": "Expense updated successfully"
    }
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"success": True, "message": "Expense deleted successfully"}


