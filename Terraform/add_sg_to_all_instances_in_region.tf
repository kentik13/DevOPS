provider "aws" {
  region = "ca-central-1"
}

# Отримати всі інстанси у регіоні
data "aws_instances" "all" {
  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
}

# Отримати деталі для кожного інстансу
data "aws_instance" "example" {
  for_each = toset(data.aws_instances.all.ids)
  instance_id = each.value
}

# Додаємо існуючу групу безпеки до всіх інтерфейсів інстансів
resource "aws_network_interface_sg_attachment" "example" {
  for_each = data.aws_instance.example

  security_group_id    = "sg-057e9e11190401773"
  network_interface_id = each.value.network_interface_id
}
