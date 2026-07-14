import sys
import os
import shutil

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from detector import DriftDetector

def test_apply_fix():
    # Setup test directory
    test_dir = "test_tf_dir"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Create main.tf
    main_tf_path = os.path.join(test_dir, "main.tf")
    with open(main_tf_path, "w") as f:
        f.write('resource "aws_vpc" "main" {\n  cidr_block = "10.0.0.0/16"\n}\n')
        
    detector = DriftDetector(tf_dir=test_dir)
    
    # 1. Test modifying existing block in main.tf
    new_vpc_hcl = 'resource "aws_vpc" "main" {\n  cidr_block = "10.0.0.0/16"\n  enable_dns_support = true\n}\n'
    detector.apply_fix(new_vpc_hcl, "main.tf")
    
    with open(main_tf_path, "r") as f:
        content = f.read()
        assert "enable_dns_support = true" in content
        
    # 2. Test appending new block to main.tf
    new_subnet_hcl = 'resource "aws_subnet" "sub1" {\n  vpc_id = aws_vpc.main.id\n}\n'
    detector.apply_fix(new_subnet_hcl, "main.tf")
    
    with open(main_tf_path, "r") as f:
        content = f.read()
        assert "aws_subnet" in content
        
    # 3. Test creating entirely new file
    new_s3_hcl = 'resource "aws_s3_bucket" "b" {\n  bucket = "my-bucket"\n}\n'
    detector.apply_fix(new_s3_hcl, "storage.tf")
    
    storage_tf_path = os.path.join(test_dir, "storage.tf")
    assert os.path.exists(storage_tf_path)
    with open(storage_tf_path, "r") as f:
        content = f.read()
        assert "aws_s3_bucket" in content
        
    # Cleanup
    shutil.rmtree(test_dir)
    print("All apply_fix multi-file tests passed successfully!")

if __name__ == "__main__":
    test_apply_fix()
