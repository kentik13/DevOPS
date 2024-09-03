provider "aws" {
  region = "ca-central-1"  # Вкажіть ваш регіон
}

# Отримання всіх інстансів за допомогою data source
data "aws_instances" "all" {}

# Отримання інформації про кожен інстанс через data source
data "aws_instance" "example" {
  for_each = toset(data.aws_instances.all.ids)
  instance_id = each.key
}

# Виведення списку інстансів та їх груп безпеки
output "instance_security_groups" {
  value = [
    for instance in data.aws_instance.example : {
      instance_id     = instance.instance_id
      security_groups = instance.vpc_security_group_ids
    }
  ]
}
