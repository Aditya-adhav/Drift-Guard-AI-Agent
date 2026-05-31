import os
import sys
from detector import DriftDetector

if __name__ == "__main__":
    detector = DriftDetector(tf_dir="c:/Users/adity/OneDrive/Desktop/drift")
    plan_output = "Terraform will perform the following actions: + resource \"aws_s3_bucket\" \"new_bucket\" { + bucket = \"new-bucket-name\" }"
    result = detector.analyze_and_remediate(plan_output)
    print("Result:", result)
