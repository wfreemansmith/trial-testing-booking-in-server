
# 🧱 SQL to SQLAlchemy ORM Comparison Guide

## Table & Column Definitions

**SQL**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);
```

**SQLAlchemy**
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
```

---

## Foreign Keys & Relationships

**SQL**
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title TEXT
);
```

**SQLAlchemy**
```python
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(Text)
    user = relationship("User", back_populates="posts")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="user")
```

---

## Unique Constraints & Indexes

**SQL**
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE
);
CREATE INDEX idx_name ON employees(name);
```

**SQLAlchemy**
```python
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, unique=True)
```

---

## Composite Primary Keys / Unique Constraints

**SQL**
```sql
CREATE TABLE enrollment (
    student_id INT,
    course_id INT,
    PRIMARY KEY(student_id, course_id)
);
```

**SQLAlchemy**
```python
class Enrollment(Base):
    __tablename__ = "enrollment"
    student_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, primary_key=True)
```

**For Unique Constraint Instead**
```python
__table_args__ = (UniqueConstraint("student_id", "course_id"),)
```

---

## Timestamps & Defaults

**SQL**
```sql
created_at TIMESTAMP DEFAULT NOW()
```

**SQLAlchemy**
```python
from sqlalchemy.sql import func
created_at = Column(DateTime, server_default=func.now())
```
