import os
import sys
import click

from beltbuckle.templates import copy_and_replace

@click.command()
@click.option('--template', default=None, help='Template to instantiate.', required=True)
@click.option('--dest', default=None, help='Destination to instantiate template into.', required=True)
@click.option('--name', default=None, help='Name of instantiated project.', required=True)

def main(template, dest, name) -> None:
  print(f"template: {template}, dest: {dest}, name: {name}")
  abs_dir_of_caller = os.path.dirname(os.path.abspath(sys.argv[0]))
  template_directory = os.path.abspath(os.path.join(abs_dir_of_caller, template))
  template_destination = os.path.abspath(os.path.join(abs_dir_of_caller, dest))
  template_destination = os.path.join(template_destination, os.path.basename(template_directory))
  print(f"instantiating template_directory: {template_directory} to template_destination: {template_destination}")
  copy_and_replace(template_directory, template_destination, "beltbuckle", name)

if __name__ == "__main__":
  main()
