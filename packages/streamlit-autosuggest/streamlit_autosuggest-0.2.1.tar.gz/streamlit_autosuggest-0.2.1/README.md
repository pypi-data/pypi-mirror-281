# Streamlit Autosuggest Component

A custom Streamlit component that provides a searchbar with autosuggestions functionality.

## Installation

You can install the streamlit-autosuggest component using pip:

    pip install streamlit-autosuggest

## Usage

Here's a simple example of how to use the searchbar component in your Streamlit app:

    import streamlit as st
    from streamlit_autosuggest import searchbar

    st.title("Autosuggest Component Demo")

    # Use the searchbar component
    result = searchbar(suggestions=['apple', 'banana', 'cherry'], placeholder="Type a fruit name", key="demo_searchbar")

    # Display the search result
    if result:
        st.write("You searched for:", result)

## Features

- Autocomplete suggestions as you type
- Customizable suggestions list
- Customizable placeholder text
- Seamless integration with existing Streamlit applications

## API Reference

### searchbar(suggestions=None, placeholder=None, key=None)

Creates a new instance of the searchbar component.

Parameters:
- suggestions (list of str, optional): A list of suggestions for the searchbar.
- placeholder (str, optional): A placeholder text for the searchbar.
- key (str, optional): An optional key that uniquely identifies this component.

Returns:
- str: The selected or typed value in the searchbar.

## Development

To contribute to this project, please see the GitHub repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Developed by Chris Weeks
