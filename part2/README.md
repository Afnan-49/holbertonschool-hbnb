# HBnB Evolution: Part 2 — Business Logic & API Layer
## 📖 Table of Contents
- Introduction
- Architecture & Design Patterns
- Technical Implementation Details
- The Business Logic Layer (Models)
- The Persistence Layer (Repository)
- The Service Layer (Facade)
- The Presentation Layer (API)
- API Endpoints Reference
- Testing and Validation
- Installation and Setup
-----------------------------------
## 📖 Introduction
HBnB Evolution is a modular vacation rental management system. In this second phase of development, we have implemented the core Business Logic and the RESTful API. This implementation emphasizes a clean separation of concerns, ensuring that each component—from user management to place reviews—is decoupled and independently testable.
-----------------------------------
## 🏗️ Architecture & Design Patterns
The project follows a 3-Tier Architecture (Presentation, Business Logic, and Persistence) connected via the Facade Pattern.

## 🛠️ Key Patterns Used:
- Facade Pattern: The HBnBFacade acts as a single point of entry for the API, coordinating operations between the models and the repositories.
- Repository Pattern: We use an InMemoryRepository to abstract data storage. This allows the system to remain storage-agnostic; we can swap the in-memory dictionary for a      database in the future without changing the logic.
- Singleton Pattern: The facade is instantiated once and shared across the application to maintain a consistent state.
- Data Transfer Objects (DTOs): We use serialize_... methods in the API layer to format model data into JSON, ensuring internal logic doesn't leak to the client.
--------------------------------------------
## 🛠️ Technical Implementation Details
1. The Business Logic Layer (Models)
All entities (User, Place, Review, Amenity) inherit from a BaseModel that provides:
A unique uuid4 identifier.
created_at and updated_at timestamps.
An update() method for bulk attribute modification.

## 🛡️ Robust Validation (validators.py)
Data integrity is enforced at the model level using custom validator functions. Every time a model is created or updated, the validate() method is called to ensure:
Users: Valid email formats and required names.
Places: Price must be positive; Latitude (-90 to 90) and Longitude (-180 to 180) must be within geo-spatial bounds.
Reviews: Ratings must be between 1 and 5.

2. The Persistence Layer (Repository)
We implemented a generic Repository Abstract Base Class (ABC) to define the interface for data operations (add, get, get_all, update, delete). The InMemoryRepository currently manages these objects in a dictionary, providing fast access for development.

3. The Service Layer (Facade)
The HBnBFacade handles the "heavy lifting" of the application:
User Management: Ensures email uniqueness before adding a user.
Place Management: Validates that an owner_id exists and that all provided amenity_ids are valid before creating a place.
Review Management: Automatically updates the Place model's review collection when a new review is created.

4. The Presentation Layer (API)
Built with Flask-RESTx, the API is organized into Namespaces:
Documentation: Automatic Swagger UI generation (accessible at /).
Error Handling: Uses api.abort() to return clear, standard HTTP error codes (400 for bad data, 404 for missing resources).
---
## 🌐 API Endpoints Reference
Method,Endpoint,Description
POST,/users/,Create a new user
GET,/users/,List all users
GET,/users/<id>,Get user details
PUT,/users/<id>,Update user info
---
### **Users**

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/users/` | Create a new user |
| **GET** | `/users/` | List all users |
| **GET** | `/users/<id>` | Get user details |
| **PUT** | `/users/<id>` | Update user info |
---
### **Places**

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/places/` | Register a new place (validates owner & amenities) |
| **GET** | `/places/` | List all places |
| **GET** | `/places/<id>` | Detailed place view (includes owner details & amenities) |
| **PUT** | `/places/<id>` | Update place information |
---
### **Reviews**

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/reviews/` | Create a review for a place |
| **GET** | `/reviews/` | List all reviews |
| **GET** | `/reviews/<id>` | Get specific review details |
| **DELETE** | `/reviews/<id>` | Delete a review (updates the Place's review list) |
| **GET** | `/reviews/places/<id>/reviews` | Get all reviews for a specific place |                                                                                           ---                                                                                                                                                                           ### 🧪 Running Tests

To run the basic model tests, execute the following command in your terminal:

```bash
python3 tests/test_models_basic.py
```
---

### 🛠️ Manual Testing with cURL

You can test the API directly using `curl`. Run the following command in your terminal to register a new user:

## Register a User

```
curl -X POST "[http://127.0.0.1:5000/users/](http://127.0.0.1:5000/users/)" \
     -H "Content-Type: application/json" \
     -d '{
          "first_name": "John",
          "last_name": "Doe",
          "email": "john.doe@example.com",
          "password": "securepassword"
         }'
```
---
🚦 Installation and Setup
1. Clone the Repository:
```
git clone <repository_url>
cd part2
```
2. Setup Virtual Environment:
```
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies:
```
pip install -r requirements.txt
```
4. Run the Application:
```
python run.py
```
The API will be available at http://0.0.0.0:5000/.
---
## 👥 Authors
* **Afnan Alfaidi** - [GitHub Profile](https://github.com/Afnan2049)
* **Lara Alzannan** - [GitHub Profile](https://github.com/laradreamer79)
---
