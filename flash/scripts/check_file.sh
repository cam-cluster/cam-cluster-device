function check_file {
  local file_path=$1
  if [[ ! -f "$file_path" ]]; then
    echo "Error: Cannot find file \"${file_path}\""
    echo
    return -2
  else
    return 0
  fi
}
