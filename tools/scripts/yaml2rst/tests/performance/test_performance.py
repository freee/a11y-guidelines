"""Performance tests for yaml2rst."""
import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path
import time
import psutil
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from yaml2rst.generators.file_generator import FileGenerator, GeneratorConfig
from yaml2rst.generators.base_generator import BaseGenerator


class TestPerformance:
    """Performance tests for yaml2rst components."""

    @pytest.mark.slow
    def test_large_dataset_generation_performance(self, mock_templates):
        """Test performance with large dataset."""
        # Create a generator that yields many items
        class LargeDatasetGenerator(BaseGenerator):
            def __init__(self, lang, item_count=1000):
                super().__init__(lang)
                self.item_count = item_count
            
            def generate(self):
                for i in range(self.item_count):
                    yield {
                        'filename': f'item_{i:04d}',
                        'title': f'Item {i}',
                        'content': f'Content for item {i}' * 100,  # Make content larger
                        'metadata': {
                            'id': f'item_{i}',
                            'priority': 'high' if i % 3 == 0 else 'medium',
                            'category': f'category_{i % 10}',
                            'tags': [f'tag_{j}' for j in range(i % 5)]
                        }
                    }
        
        # Setup FileGenerator
        file_generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=LargeDatasetGenerator,
            template_name='category_page',
            output_path='/tmp/test_output',
            is_single_file=False,
            extra_args={'item_count': 1000}
        )
        
        # Measure performance
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        file_generator.generate(config, build_all=True, targets=[])
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        execution_time = end_time - start_time
        memory_usage = end_memory - start_memory
        
        # Performance assertions
        assert execution_time < 10.0, f"Generation took too long: {execution_time:.2f}s"
        assert memory_usage < 100, f"Memory usage too high: {memory_usage:.2f}MB"
        
        # Verify all items were processed
        template = mock_templates['category_page']
        assert template.write_rst.call_count == 1000

    @pytest.mark.slow
    def test_memory_usage_with_large_files(self, mock_templates):
        """Test memory usage with large file content."""
        class LargeContentGenerator(BaseGenerator):
            def __init__(self, lang):
                super().__init__(lang)
            
            def generate(self):
                # Generate files with large content
                large_content = "x" * (1024 * 1024)  # 1MB of content per file
                
                for i in range(10):
                    yield {
                        'filename': f'large_file_{i}',
                        'title': f'Large File {i}',
                        'content': large_content,
                        'additional_data': {
                            'large_list': list(range(10000)),
                            'large_dict': {f'key_{j}': f'value_{j}' for j in range(1000)}
                        }
                    }
        
        file_generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=LargeContentGenerator,
            template_name='category_page',
            output_path='/tmp/test_output',
            is_single_file=False
        )
        
        # Monitor memory usage
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        file_generator.generate(config, build_all=True, targets=[])
        
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory
        
        # Memory should not increase excessively
        assert memory_increase < 200, f"Memory increase too high: {memory_increase:.2f}MB"

    def test_generator_initialization_performance(self):
        """Test performance of generator initialization."""
        class TestGenerator(BaseGenerator):
            def __init__(self, lang):
                super().__init__(lang)
                # Simulate some initialization work
                self.data = list(range(10000))
            
            def generate(self):
                yield {'filename': 'test', 'content': 'test'}
        
        # Measure initialization time
        start_time = time.time()
        
        for _ in range(100):
            generator = TestGenerator('ja')
        
        end_time = time.time()
        
        avg_init_time = (end_time - start_time) / 100
        
        # Initialization should be fast
        assert avg_init_time < 0.01, f"Generator initialization too slow: {avg_init_time:.4f}s"

    @pytest.mark.slow
    def test_concurrent_generation_performance(self, mock_templates):
        """Test performance with concurrent-like generation patterns."""
        import threading
        import queue
        
        class ConcurrentTestGenerator(BaseGenerator):
            def __init__(self, lang, thread_id=0):
                super().__init__(lang)
                self.thread_id = thread_id
            
            def generate(self):
                for i in range(100):
                    yield {
                        'filename': f'thread_{self.thread_id}_item_{i}',
                        'content': f'Content from thread {self.thread_id}, item {i}',
                        'thread_id': self.thread_id
                    }
        
        # Simulate concurrent generation
        results_queue = queue.Queue()
        
        def generate_worker(thread_id):
            file_generator = FileGenerator(mock_templates, 'ja')
            config = GeneratorConfig(
                generator_class=ConcurrentTestGenerator,
                template_name='category_page',
                output_path=f'/tmp/test_output_{thread_id}',
                is_single_file=False,
                extra_args={'thread_id': thread_id}
            )
            
            start_time = time.time()
            file_generator.generate(config, build_all=True, targets=[])
            end_time = time.time()
            
            results_queue.put(end_time - start_time)
        
        # Run multiple "concurrent" generations
        threads = []
        num_threads = 5
        
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=generate_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        # Collect individual times
        individual_times = []
        while not results_queue.empty():
            individual_times.append(results_queue.get())
        
        avg_individual_time = sum(individual_times) / len(individual_times)
        
        # Performance assertions
        assert total_time < 30.0, f"Concurrent generation took too long: {total_time:.2f}s"
        assert avg_individual_time < 10.0, f"Individual generation too slow: {avg_individual_time:.2f}s"

    def test_template_rendering_performance(self, mock_templates):
        """Test template rendering performance."""
        # Create a generator with complex data
        class ComplexDataGenerator(BaseGenerator):
            def __init__(self, lang):
                super().__init__(lang)
            
            def generate(self):
                complex_data = {
                    'filename': 'complex_file',
                    'title': 'Complex File',
                    'nested_data': {
                        'level1': {
                            'level2': {
                                'level3': {
                                    'items': [{'id': i, 'name': f'Item {i}'} for i in range(1000)]
                                }
                            }
                        }
                    },
                    'large_list': list(range(5000)),
                    'metadata': {f'key_{i}': f'value_{i}' for i in range(1000)}
                }
                yield complex_data
        
        file_generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=ComplexDataGenerator,
            template_name='category_page',
            output_path='/tmp/test_output',
            is_single_file=False
        )
        
        # Measure template rendering performance
        start_time = time.time()
        
        file_generator.generate(config, build_all=True, targets=[])
        
        end_time = time.time()
        
        rendering_time = end_time - start_time
        
        # Template rendering should be reasonably fast
        assert rendering_time < 5.0, f"Template rendering too slow: {rendering_time:.2f}s"

    def test_selective_generation_performance(self, mock_templates):
        """Test performance of selective generation vs full generation."""
        class ManyFilesGenerator(BaseGenerator):
            def __init__(self, lang):
                super().__init__(lang)
            
            def generate(self):
                for i in range(1000):
                    yield {
                        'filename': f'file_{i:04d}',
                        'content': f'Content for file {i}'
                    }
        
        file_generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=ManyFilesGenerator,
            template_name='category_page',
            output_path='/tmp/test_output',
            is_single_file=False
        )
        
        # Test full generation
        start_time = time.time()
        file_generator.generate(config, build_all=True, targets=[])
        full_generation_time = time.time() - start_time
        
        # Reset mock
        mock_templates['category_page'].write_rst.reset_mock()
        
        # Test selective generation (only 10 files)
        targets = [f'/tmp/test_output/file_{i:04d}.rst' for i in range(10)]
        
        start_time = time.time()
        file_generator.generate(config, build_all=False, targets=targets)
        selective_generation_time = time.time() - start_time
        
        # Selective generation should be much faster
        # Note: This test might not show significant difference with mocks,
        # but it tests the code path
        assert selective_generation_time <= full_generation_time
        
        # Verify only targeted files were processed
        assert mock_templates['category_page'].write_rst.call_count == 10

    @pytest.mark.slow
    def test_memory_leak_detection(self, mock_templates):
        """Test for memory leaks during repeated generation."""
        class SimpleGenerator(BaseGenerator):
            def __init__(self, lang):
                super().__init__(lang)
            
            def generate(self):
                for i in range(100):
                    yield {
                        'filename': f'file_{i}',
                        'content': f'Content {i}',
                        'data': list(range(1000))  # Some data that should be cleaned up
                    }
        
        file_generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=SimpleGenerator,
            template_name='category_page',
            output_path='/tmp/test_output',
            is_single_file=False
        )
        
        # Measure memory before
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Run generation multiple times
        for iteration in range(10):
            file_generator.generate(config, build_all=True, targets=[])
            mock_templates['category_page'].write_rst.reset_mock()
            
            # Check memory periodically
            if iteration % 3 == 0:
                current_memory = psutil.Process().memory_info().rss / 1024 / 1024
                memory_increase = current_memory - initial_memory
                
                # Memory should not grow excessively
                assert memory_increase < 50, f"Potential memory leak detected: {memory_increase:.2f}MB increase"

    def test_error_handling_performance(self, mock_templates):
        """Test that error handling doesn't significantly impact performance."""
        class ErrorProneGenerator(BaseGenerator):
            def __init__(self, lang):
                super().__init__(lang)
            
            def generate(self):
                for i in range(100):
                    if i % 10 == 0:
                        # This will cause validation to fail
                        yield {'filename': f'bad_file_{i}'}  # Missing required fields
                    else:
                        yield {
                            'filename': f'good_file_{i}',
                            'content': f'Good content {i}'
                        }
            
            def validate_data(self, data):
                return 'content' in data
        
        file_generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=ErrorProneGenerator,
            template_name='category_page',
            output_path='/tmp/test_output',
            is_single_file=False
        )
        
        # Measure performance with error handling
        start_time = time.time()
        
        try:
            file_generator.generate(config, build_all=True, targets=[])
        except Exception:
            pass  # Expected to fail due to validation errors
        
        end_time = time.time()
        
        error_handling_time = end_time - start_time
        
        # Error handling should not make it excessively slow
        assert error_handling_time < 10.0, f"Error handling too slow: {error_handling_time:.2f}s"


class TestScalability:
    """Test scalability of yaml2rst components."""

    @pytest.mark.slow
    @pytest.mark.parametrize("item_count", [100, 500, 1000])
    def test_generation_scales_linearly(self, mock_templates, item_count):
        """Test that generation time scales roughly linearly with item count."""
        class ScalabilityTestGenerator(BaseGenerator):
            def __init__(self, lang, count):
                super().__init__(lang)
                self.count = count
            
            def generate(self):
                for i in range(self.count):
                    yield {
                        'filename': f'item_{i}',
                        'content': f'Content for item {i}'
                    }
        
        file_generator = FileGenerator(mock_templates, 'ja')
        
        config = GeneratorConfig(
            generator_class=ScalabilityTestGenerator,
            template_name='category_page',
            output_path='/tmp/test_output',
            is_single_file=False,
            extra_args={'count': item_count}
        )
        
        start_time = time.time()
        file_generator.generate(config, build_all=True, targets=[])
        end_time = time.time()
        
        generation_time = end_time - start_time
        time_per_item = generation_time / item_count
        
        # Time per item should be reasonable and consistent
        assert time_per_item < 0.1, f"Time per item too high: {time_per_item:.4f}s"
        
        # Verify all items were processed
        assert mock_templates['category_page'].write_rst.call_count == item_count

    def test_memory_usage_scales_reasonably(self, mock_templates):
        """Test that memory usage doesn't grow excessively with data size."""
        class MemoryTestGenerator(BaseGenerator):
            def __init__(self, lang, data_size_mb):
                super().__init__(lang)
                self.data_size_mb = data_size_mb
            
            def generate(self):
                # Create data of specified size
                data_size_bytes = self.data_size_mb * 1024 * 1024
                large_content = "x" * data_size_bytes
                
                yield {
                    'filename': 'large_file',
                    'content': large_content
                }
        
        # Test with different data sizes
        for data_size in [1, 5, 10]:  # MB
            initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            file_generator = FileGenerator(mock_templates, 'ja')
            
            config = GeneratorConfig(
                generator_class=MemoryTestGenerator,
                template_name='category_page',
                output_path='/tmp/test_output',
                is_single_file=False,
                extra_args={'data_size_mb': data_size}
            )
            
            file_generator.generate(config, build_all=True, targets=[])
            
            final_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_increase = final_memory - initial_memory
            
            # Memory increase should be reasonable relative to data size
            # Allow for some overhead, but not excessive
            max_expected_memory = data_size * 3  # 3x overhead should be reasonable
            assert memory_increase < max_expected_memory, \
                f"Memory usage too high for {data_size}MB data: {memory_increase:.2f}MB"
            
            # Reset for next iteration
            mock_templates['category_page'].write_rst.reset_mock()
