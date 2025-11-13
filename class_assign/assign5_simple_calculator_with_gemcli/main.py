from fastapi import FastAPI
from calculator import ScientificCalculator

app = FastAPI()
calc = ScientificCalculator()

@app.get("/add")
def add(x: float, y: float):
    return {"result": calc.add(x, y)}

@app.get("/subtract")
def subtract(x: float, y: float):
    return {"result": calc.subtract(x, y)}

@app.get("/multiply")
def multiply(x: float, y: float):
    return {"result": calc.multiply(x, y)}

@app.get("/divide")
def divide(x: float, y: float):
    try:
        return {"result": calc.divide(x, y)}
    except ValueError as e:
        return {"error": str(e)}

@app.get("/sin")
def sin(x: float):
    return {"result": calc.sin(x)}

@app.get("/cos")
def cos(x: float):
    return {"result": calc.cos(x)}

@app.get("/tan")
def tan(x: float):
    return {"result": calc.tan(x)}

@app.get("/log")
def log(x: float):
    try:
        return {"result": calc.log(x)}
    except ValueError as e:
        return {"error": str(e)}

@app.get("/sqrt")
def sqrt(x: float):
    try:
        return {"result": calc.sqrt(x)}
    except ValueError as e:
        return {"error": str(e)}
