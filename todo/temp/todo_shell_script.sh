#!/bin/zsh

# Set colors
CYAN="\033[36m"
BOLD="\033[1m"
RESET="\033[0m"

# Give first argument to variable
FLAG=$1
ARG=$2

# Activate virtual environment
echo "${CYAN}==> Activate virtual environment ${BOLD}utils_env${RESET}"
### !!! ADD EXISTING PYTHON ENVIRONMENT !!! ###
# Use `python3 -m venv <name-of-my-virt-env>`
# Of course you can use a conda environment and then use
# `conda <my-virt-env> activate`
source ~/<MY-PYTHON-ENV>/bin/activate

# Start ToDo script
echo "${CYAN}Start ${BOLD}ToDo${RESET}"
python3 ~/repositories/codeberg/utilities/todo/main.py "${FLAG} ${ARG}"

echo "${CYAN}==> Ended ${BOLD}ToDo${RESET}"

# Deactivate virtual environment
echo "${CYAN}==> Deactivate virtual environment${RESET}"
deactivate
