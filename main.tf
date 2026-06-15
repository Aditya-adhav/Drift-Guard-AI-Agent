resource "aws_security_group" "test_sg" {
  name        = "drift-guard-test-sg"
  description = "Testing drift guard"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/16"]
  }
}