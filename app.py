import os
from neo4j import GraphDatabase
import streamlit as st

# Aura database connection class
class AuraDatabase:
    def __init__(self):
        uri = os.getenv("AURA_URI", "")
        user = os.getenv("AURA_USER", "")
        password = os.getenv("AURA_PASSWORD", "")
        if not uri or not user or not password:
            raise ValueError("Please set AURA_URI, AURA_USER, and AURA_PASSWORD environment variables.")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver:
            self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters)

# Neo4j MCP server query function
def query_mcp_server(query):
    mcp_server_url = os.getenv("MCP_SERVER_URL", "")
    if not mcp_server_url:
        raise ValueError("Please set MCP_SERVER_URL environment variable.")

    # Simulate a request to the MCP server (replace with actual HTTP request logic)
    return f"MCP server response for query: {query}"

def main():
    st.title("Research Paper Search and Chatbot")

    # Sidebar for search criteria
    st.sidebar.header("Search Criteria")
    keyword = st.sidebar.text_input("Keyword", "")
    author = st.sidebar.text_input("Author", "")
    year = st.sidebar.number_input("Year", min_value=1900, max_value=2025, step=1, value=2025)

    # Search button
    if st.sidebar.button("Search"):
        st.write(f"Searching for papers with keyword: {keyword}, author: {author}, year: {year}")
        try:
            db = AuraDatabase()
            result = db.query("MATCH (n) RETURN n LIMIT 5")
            st.write("Results from Aura database:")
            for record in result:
                st.write(record)
            db.close()
        except ValueError as e:
            st.error(str(e))

    # Chatbot section
    st.header("Chat with the Assistant")
    user_input = st.text_input("Ask something about your search:", "")
    if st.button("Send"):
        try:
            response = query_mcp_server(user_input)
            st.write(response)
        except ValueError as e:
            st.error(str(e))

if __name__ == "__main__":
    main()