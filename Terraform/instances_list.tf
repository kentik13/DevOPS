provider "aws" {
  region = "ca-central-1"  # Specify your region
}

# Data source to fetch all EC2 instances
data "aws_instances" "all" {}

# Fetch details for each instance using its ID
data "aws_instance" "details" {
  for_each = toset(data.aws_instances.all.ids)

  instance_id = each.key
}

# Output instance IDs and names
output "instance_details" {
  value = [
    for instance in data.aws_instance.details :
    {
      id   = instance.id
      name = lookup(instance.tags, "Name", "No Name")
    }
  ]
}
