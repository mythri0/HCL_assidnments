# Assignment 02 – Library Book Loan Dimensional Modeling

## 1. Project Overview

This assignment focuses on designing a dimensional data model for a local library to analyze book loan activities, popular genres, and member engagement.

The objective is to apply data warehousing concepts such as fact tables, dimension tables, grain, measures, and star schema design.

## 2. Business Process

**Business Process: Book Loan**

The selected business process is the book loan transaction in a library.

Whenever a library member borrows a book, a loan transaction is recorded. The library can use this information to understand borrowing patterns, identify popular books and genres, analyze member activity, and monitor overdue returns.

### Business Questions

The dimensional model helps answer the following questions:

- Which book genres are borrowed most frequently?
- Which books are the most popular?
- Which members borrow the most books?
- What is the average book loan duration?
- How many books are returned late?
- During which months does the library experience the highest borrowing activity?

## 3. Grain Definition

**Chosen Grain: One row per individual book loan transaction.**

Each record in the `Fact_Book_Loan` table represents one book borrowed by one library member on a particular loan date.

For example, if a member borrows three different books, three separate records will be created in the fact table.

Defining the grain ensures that every fact record represents the same level of business activity.

## 4. Fact Table – Fact_Book_Loan

The fact table is the central table in the dimensional model. It stores measurable information about each book loan transaction and contains foreign keys connecting it to the dimension tables.

| Attribute | Description |
|---|---|
| Loan_ID | Unique loan transaction identifier |
| Book_Key | Foreign key referencing Dim_Book |
| Member_Key | Foreign key referencing Dim_Member |
| Loan_Date_Key | Foreign key referencing Dim_Date |
| Due_Date_Key | Foreign key referencing Dim_Date |
| Return_Date_Key | Foreign key referencing Dim_Date |
| Loan_Count | Number of loan transactions (1 per row) |
| Loan_Duration_Days | Number of days between borrowing and returning |
| Overdue_Days | Number of days returned after the due date |
| Renewal_Count | Number of times a loan was renewed |

### Fact Measures

1. **Loan_Count:** Counts the total number of book loan transactions.
2. **Loan_Duration_Days:** Measures the duration for which a member keeps a borrowed book.
3. **Overdue_Days:** Measures how many days a book is returned after its due date.
4. **Renewal_Count:** Measures how many times a loan has been renewed.

*Note: Loan duration and overdue days can be calculated when a book is returned. For active loans, these measures may remain NULL until the return occurs.*

## 5. Dimension Tables

Dimension tables contain descriptive attributes that provide context to the fact table.

### 5.1 Dim_Book

**Purpose:** Stores descriptive information about books available in the library.

| Attribute | Description |
|---|---|
| Book_Key (PK) | Unique book dimension key |
| Book_ID | Original book identifier |
| Book_Title | Title of the book |
| Author | Author name |
| Genre | Book category or genre |
| Publisher | Publisher name |
| Publication_Year | Year of publication |

### 5.2 Dim_Member

**Purpose:** Stores descriptive information about library members.

| Attribute | Description |
|---|---|
| Member_Key (PK) | Unique member dimension key |
| Member_ID | Original member identifier |
| Member_Name | Member's name |
| Membership_Type | Type of membership |
| Age_Group | Member's age category |
| City | Member's city |
| Join_Date | Date the member joined the library |

### 5.3 Dim_Date

**Purpose:** Stores calendar-related information to support time-based analysis.

| Attribute | Description |
|---|---|
| Date_Key (PK) | Unique date dimension key |
| Full_Date | Complete calendar date |
| Day | Day of the month |
| Month | Month name |
| Quarter | Calendar quarter |
| Year | Calendar year |
| Weekday | Day of the week |

The same Dim_Date dimension is reused for the loan date, due date, and return date. These are known as **role-playing dimensions**.

## 6. Star Schema Architecture

The dimensional model follows a Star Schema design.

The `Fact_Book_Loan` table is positioned at the centre and connects to three dimension tables:

- Dim_Book
- Dim_Member
- Dim_Date

Each dimension has a one-to-many relationship with the fact table. Dim_Date is referenced through three different date roles.

### Relationship Overview

| Dimension Table | Fact Table Foreign Key | Relationship |
|---|---|---|
| Dim_Book | Book_Key | One-to-Many |
| Dim_Member | Member_Key | One-to-Many |
| Dim_Date | Loan_Date_Key | One-to-Many |
| Dim_Date | Due_Date_Key | One-to-Many |
| Dim_Date | Return_Date_Key | One-to-Many |

### Star Schema Diagram

![Library Book Loan Star Schema](design/library_star_schema.png)

## 7. Expected Analytical Benefits

This dimensional model allows the library to:

- Identify the most popular books and genres.
- Analyze borrowing activity by month, quarter, and year.
- Measure member engagement and borrowing frequency.
- Calculate average loan duration.
- Identify overdue book return patterns.
- Compare borrowing trends across membership types.

## 8. Repository Structure

```text
Assignment-02/
│
├── README.md
│
├── design/
│   ├── library_star_schema.drawio
│   └── library_star_schema.png
│
└── screenshots/
    └── completed_design.png
```

## 9. Tools Used

- **diagrams.net (draw.io):** For designing the star schema diagram.
- **GitHub:** For storing and submitting the assignment.
- **Markdown:** For documenting the dimensional model.

## 10. Key Learnings

Through this assignment, I learned how to identify a business process, define the grain of a fact table, distinguish fact measures from descriptive dimensions, establish primary and foreign key relationships, and design a dimensional model using the Star Schema approach.

I also understood the concept of role-playing dimensions through the reuse of the date dimension for multiple business events.

---

**Assignment:** 02 – Library Book Loan Dimensional Modeling  
**Domain:** Data Warehousing and Dimensional Modeling  
**Author:** Balaji Suriya V.