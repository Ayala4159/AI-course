# Development Guidelines and Best Practices

## Code Style

### Python Version
- Minimum: Python 3.9
- Recommended: Python 3.11+
- Uses modern Python features (type hints, f-strings, dataclass-compatible patterns)

### Naming Conventions

#### Classes
- PascalCase (e.g., `TaskManager`, `TaskPriority`)
- Exception classes end with `Error` (e.g., `TaskNotFoundError`)

#### Functions and Methods
- snake_case (e.g., `add_task`, `get_pending_tasks`)
- Private methods start with underscore (e.g., `_validate_input`)

#### Constants
- UPPER_SNAKE_CASE

### Docstring Format
All modules, classes, and public methods use docstrings:

```python
def add_task(self, title: str, description: str) -> Task:
    """Add a new task to the manager.
    
    Args:
        title: Task title
        description: Task description
        
    Returns:
        The created task object
    """
```

## Testing Strategy

### Test Coverage
Target minimum 80% code coverage using pytest-cov:

```bash
pytest --cov=src tests/
```

### Test Organization
- `tests/test_task.py`: Unit tests for Task class
- `tests/test_task_manager.py`: Unit tests for TaskManager class
- Each test method tests a single logical unit
- Use descriptive test names like `test_mark_completed()`

### Test Structure (AAA Pattern)
```python
def test_something(self):
    # Arrange
    task = Task(1, "Title", "Desc")
    
    # Act
    task.mark_completed()
    
    # Assert
    self.assertEqual(task.status, TaskStatus.COMPLETED)
```

## Common Development Tasks

### Adding a New Feature
1. Define the feature in design documents
2. Write tests for the feature
3. Implement the feature
4. Run tests to verify
5. Update docstrings
6. Update this guide if applicable

### Running Tests
```bash
# All tests
python -m unittest discover tests/

# Specific test file
python -m unittest tests.test_task

# With coverage
pytest --cov=src tests/
```

### Code Quality
```bash
# Type checking
mypy src/

# Linting (if flake8 is installed)
flake8 src/
```

## Known Limitations

1. **No database backend**: Currently uses in-memory storage only
2. **Single-user**: Not designed for concurrent access
3. **No authentication**: No user/permission system
4. **Limited validation**: Basic input validation only
5. **No task relationships**: Tasks are independent

## Performance Considerations

- **Filtering**: O(n) where n is number of tasks
- **Task lookup**: O(1) via task_id in dictionary
- **File I/O**: Synchronous only

For large datasets (>1000s of tasks), consider:
- Database backend
- Pagination
- Caching strategies
- Asynchronous I/O

## Error Handling

Current approach:
- Methods return `None` or `False` for failures
- No custom exceptions raised
- Consider adding exception hierarchy in future versions

Example:
```python
task = manager.get_task(999)  # Returns None if not found
if task is None:
    print("Task not found")
```

## Documentation Standards

All code features must include:
1. Module-level docstring
2. Class-level docstring
3. Method docstrings with Args/Returns
4. Type hints for all parameters and returns

## Contributing

When contributing:
1. Follow the code style guidelines
2. Write tests for new features
3. Ensure all tests pass
4. Update documentation
5. Use meaningful commit messages
