function parse_placeholders {
  local file_path=$1

  file_contents="$(<$file_path)"

  # Find all <placeholder> tags
  placeholders=()
  for text in ${file_contents}; do
    if [[ "$text" =~ \<(.+)\> ]]; then
      placeholders+=(${BASH_REMATCH[1]})
    fi
  done

  # Get values for each <placeholder>
  placeholder_values=()
  for placeholder in ${placeholders[@]}; do
    read -p "  ${placeholder}: " value
    placeholder_values+=("$value")
  done

  ## Replace each <placeholder> with its value
  for i in "${!placeholders[@]}"; do 
    file_contents=${file_contents//"<${placeholders[i]}>"/"${placeholder_values[i]}"}
  done

  echo "$file_contents"
}
