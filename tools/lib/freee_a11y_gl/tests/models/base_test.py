import pytest
from pathlib import Path
from freee_a11y_gl.models.base import BaseModel


@pytest.mark.usefixtures("setup_categories", "setup_faq_tags", "setup_wcag_sc", "all_check_data")
class BaseModelTest:
    """Base test class for model tests.
    
    This class provides common test patterns for models that inherit from BaseModel.
    Subclasses must set the following class attributes:
    - model_class: The model class to test
    - sample_data: A dictionary containing sample data for initialization
    """
    model_class = None
    sample_data = None

    @pytest.mark.usefixtures("setup_categories", "setup_faq_tags", "setup_wcag_sc", "all_check_data")
    def test_init(self):
        """Test basic initialization of the model."""
        if not self.model_class or not self.sample_data:
            pytest.skip("model_class or sample_data not set")

        instance = self.model_class(self.sample_data)
        assert instance.id == self.sample_data["id"]
        assert instance.sort_key == self.sample_data["sortKey"]
        assert instance.src_path == self.sample_data["src_path"]

    def test_duplicate_id(self):
        """Test that duplicate IDs raise a ValueError."""
        if not self.model_class or not self.sample_data:
            pytest.skip("model_class or sample_data not set")

        self.model_class(self.sample_data)
        model_type = self.model_class.__name__.lower()
        with pytest.raises(ValueError, match=f"Duplicate {model_type} ID: {self.sample_data['id']}"):
            self.model_class(self.sample_data)

    def test_duplicate_sort_key(self):
        """Test that duplicate sort keys raise a ValueError."""
        if not self.model_class or not self.sample_data:
            pytest.skip("model_class or sample_data not set")

        self.model_class(self.sample_data)
        duplicate_data = {
            **self.sample_data,
            "id": f"{self.sample_data['id']}_new"
        }
        model_type = self.model_class.__name__.lower()
        with pytest.raises(ValueError, match=f"Duplicate {model_type} sortKey: {self.sample_data['sortKey']}"):
            self.model_class(duplicate_data)

    def test_list_all_src_paths(self, sample_dir):
        """Test listing all source paths.
        
        Subclasses should override this if they need custom source path testing logic.
        """
        if not self.model_class or not self.sample_data:
            pytest.skip("model_class or sample_data not set")
            
        # Create an instance to ensure there's at least one source path
        self.model_class(self.sample_data)
        src_paths = self.model_class.list_all_src_paths()
        
        # Basic validation that we get a list of Path objects
        assert isinstance(src_paths, list)
        assert all(isinstance(path, (str, Path)) for path in src_paths)
        assert len(src_paths) > 0
