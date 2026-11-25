
import streamlit as st

from agent import analyze_requirements, generate_recommendation
from product_search import search_products


# Page configuration
st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛍️",
    layout="wide"
)


# Application title
st.title("🛍️ AI E-COMMERCE Shopping Assistant")

st.write(
    "Find, filter and compare products using Artificial Intelligence."
)

st.divider()


# User input
st.subheader("What are you looking for?")

user_request = st.text_area(
    "Describe your shopping requirements:",
    placeholder="Example: I need a laptop under 50000 rupees with 16GB RAM and 512GB storage for programming."
)


# Find Products button
if st.button("🔍 Find Products"):

    if not user_request.strip():

        st.warning("Please enter your shopping requirements.")

    else:

        try:

            # Step 1: Analyze requirements using Gemini AI
            with st.spinner("AI is understanding your requirements..."):

                requirements = analyze_requirements(user_request)

            st.subheader("📋 Your Requirements")

            st.json(requirements)


            # Step 2: Search matching products
            with st.spinner("Searching for matching products..."):

                products = search_products(
                    category=requirements["category"],
                    budget=requirements["budget"],
                    min_ram=requirements.get("min_ram", 0),
                    min_storage=requirements.get("min_storage", 0)
                )


            # Step 3: Display products
            st.subheader("🛒 Matching Products")

            if products.empty:

                st.warning(
                    "No matching products found. "
                    "Try changing your budget or requirements."
                )

            else:

                # Display product details and shopping links
                st.dataframe(
                    products,
                    column_config={
                        "Amazon": st.column_config.LinkColumn(
                            "Amazon",
                            display_text="View on Amazon"
                        ),

                        "Flipkart": st.column_config.LinkColumn(
                            "Flipkart",
                            display_text="View on Flipkart"
                        ),

                        "Google Shopping": st.column_config.LinkColumn(
                            "Google Shopping",
                            display_text="Compare Prices"
                        )
                    },
                    use_container_width=True,
                    hide_index=True
                )


                # Step 4: Generate AI recommendations
                with st.spinner("Generating AI recommendations..."):

                    recommendation = generate_recommendation(
                        user_request,
                        products
                    )


                st.subheader("🤖 AI Recommendations")

                st.write(recommendation)


        except Exception as e:

            st.error(f"Something went wrong: {e}")
