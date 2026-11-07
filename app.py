import streamlit as st
import requests
import json


# ==================================================
# Page configuration
# ==================================================

st.set_page_config(
    page_title="AI Lesson Creation Tool",
    page_icon="📚",
    layout="wide"
)


# ==================================================
# n8n Webhook URLs
# ==================================================

generation_webhook_url = "https://n8n.fitnesscoachbheem.co.in/webhook/kalvium-lesson"

revision_webhook_url = "https://n8n.fitnesscoachbheem.co.in/webhook/kalvium-lesson-revise"


# ==================================================
# Title
# ==================================================

st.title("AI Lesson Creation Tool")

st.write(
    "Generate, research, review, edit, validate, "
    "and improve AI-powered educational lessons."
)


# ==================================================
# Session state
# ==================================================

if "result" not in st.session_state:
    st.session_state["result"] = None

if "edited_lesson" not in st.session_state:
    st.session_state["edited_lesson"] = ""


# ==================================================
# Lesson input
# ==================================================

st.subheader("Create a Lesson")

lesson_title = st.text_input(
    "Lesson Title"
)

learning_objective = st.text_area(
    "Learning Objective",
    height=120
)


# ==================================================
# Generate lesson
# ==================================================

generate_button = st.button(
    "Generate Lesson",
    type="primary"
)


if generate_button:

    if not lesson_title.strip():

        st.error(
            "Please enter a lesson title."
        )

    elif not learning_objective.strip():

        st.error(
            "Please enter a learning objective."
        )

    else:

        payload = {
            "lesson_title": lesson_title,
            "learning_objective": learning_objective
        }

        try:

            with st.spinner(
                "Researching sources and generating lesson..."
            ):

                response = requests.post(
                    generation_webhook_url,
                    json=payload,
                    timeout=180
                )

            if response.status_code == 200:

                result = response.json()

                st.session_state["result"] = result
                st.session_state["edited_lesson"] = ""

                st.success(
                    "Lesson generated successfully!"
                )

            else:

                st.error(
                    f"Workflow failed with status code "
                    f"{response.status_code}"
                )

                st.code(response.text)

        except requests.exceptions.Timeout:

            st.error(
                "The workflow took too long to respond. "
                "Please try again."
            )

        except requests.exceptions.RequestException as error:

            st.error(
                f"Could not connect to the lesson generation "
                f"workflow: {error}"
            )

        except ValueError:

            st.error(
                "The workflow returned an invalid response."
            )


# ==================================================
# Display generated result
# ==================================================

if st.session_state["result"] is not None:

    result = st.session_state["result"]

    st.divider()


    # ==================================================
    # Lesson
    # ==================================================

    st.header("Generated Lesson")

    lesson = result.get(
        "lesson",
        {}
    )

    lesson_text = ""


    if "content" in lesson:

        parts = lesson["content"].get(
            "parts",
            []
        )

        if parts:

            lesson_text = parts[0].get(
                "text",
                ""
            )


    if not lesson_text:

        st.warning(
            "Lesson content was not found."
        )

    else:

        if st.session_state["edited_lesson"]:

            current_lesson = st.session_state[
                "edited_lesson"
            ]

        else:

            current_lesson = lesson_text


        edited_lesson = st.text_area(
            "Review and edit the lesson",
            value=current_lesson,
            height=600
        )


        # ==================================================
        # Save manual edits
        # ==================================================

        if st.button("Save Lesson Edits"):

            st.session_state[
                "edited_lesson"
            ] = edited_lesson

            st.success(
                "Lesson edits saved successfully."
            )


        # ==================================================
        # Apply QC recommendations
        # ==================================================

        if st.button(
            "Apply QC Recommendations",
            type="primary"
        ):

            qc_reports = result.get(
                "qc_reports",
                {}
            )

            qc1 = qc_reports.get(
                "factual_accuracy",
                {}
            )

            qc2 = qc_reports.get(
                "instructional_quality",
                {}
            )


            current_lesson_for_revision = (
                st.session_state["edited_lesson"]
                if st.session_state["edited_lesson"]
                else lesson_text
            )


            payload = {

                "lesson_title": result.get(
                    "lesson_title",
                    ""
                ),

                "learning_objective": result.get(
                    "learning_objective",
                    ""
                ),

                "lesson": current_lesson_for_revision,

                "qc1": qc1,

                "qc2": qc2
            }


            try:

                with st.spinner(
                    "Applying QC recommendations..."
                ):

                    revision_response = requests.post(
                        revision_webhook_url,
                        json=payload,
                        timeout=180
                    )


                if revision_response.status_code == 200:

                    revised_result = (
                        revision_response.json()
                    )

                    revised_lesson = ""


                    if "content" in revised_result:

                        parts = revised_result[
                            "content"
                        ].get(
                            "parts",
                            []
                        )

                        if parts:

                            revised_lesson = parts[0].get(
                                "text",
                                ""
                            )


                    if revised_lesson:

                        st.session_state[
                            "edited_lesson"
                        ] = revised_lesson

                        st.success(
                            "QC recommendations applied successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "The revision workflow returned "
                            "no revised lesson."
                        )

                        st.json(
                            revised_result
                        )


                else:

                    st.error(
                        f"Revision workflow failed with "
                        f"status code "
                        f"{revision_response.status_code}"
                    )

                    st.code(
                        revision_response.text
                    )


            except requests.exceptions.Timeout:

                st.error(
                    "The revision workflow took too long. "
                    "Please try again."
                )


            except requests.exceptions.RequestException as error:

                st.error(
                    f"Could not connect to the revision "
                    f"workflow: {error}"
                )


            except ValueError:

                st.error(
                    "The revision workflow returned "
                    "an invalid response."
                )


        # ==================================================
        # Preview
        # ==================================================

        if st.session_state["edited_lesson"]:

            st.subheader(
                "Saved Lesson Preview"
            )

            st.markdown(
                st.session_state["edited_lesson"]
            )


    # ==================================================
    # Research Sources
    # ==================================================

    st.divider()

    st.header("Research Sources")

    research = result.get(
        "research",
        {}
    )


    # ==================================================
    # Web Sources
    # ==================================================

    st.subheader("Web Sources")

    web_sources = research.get(
        "web_sources",
        []
    )


    if web_sources:

        for source in web_sources:

            title = source.get(
                "title",
                "Untitled Source"
            )

            url = source.get(
                "url",
                ""
            )

            if url:

                st.markdown(
                    f"- [{title}]({url})"
                )

    else:

        st.info(
            "No web sources were returned."
        )


    # ==================================================
    # Book Sources
    # ==================================================

    st.subheader("Book Sources")

    book_sources = research.get(
        "book_sources",
        []
    )


    if book_sources:

        for book in book_sources:

            title = book.get(
                "title",
                "Untitled Book"
            )

            authors = book.get(
                "authors",
                []
            )

            publisher = book.get(
                "publisher",
                ""
            )

            published_date = book.get(
                "published_date",
                ""
            )

            url = book.get(
                "url",
                ""
            )


            if isinstance(
                authors,
                list
            ):

                author_text = ", ".join(
                    authors
                )

            else:

                author_text = str(
                    authors
                )


            book_text = (
                f"**{title}**"
            )


            if author_text:

                book_text += (
                    f" — {author_text}"
                )


            if publisher:

                book_text += (
                    f" | {publisher}"
                )


            if published_date:

                book_text += (
                    f" | {published_date}"
                )


            if url:

                st.markdown(
                    f"- [{book_text}]({url})"
                )

            else:

                st.markdown(
                    f"- {book_text}"
                )

    else:

        st.info(
            "No book sources were returned."
        )


    # ==================================================
    # YouTube Sources
    # ==================================================

    st.subheader("YouTube Videos")

    youtube_videos = research.get(
        "youtube_videos",
        []
    )


    if youtube_videos:

        for video in youtube_videos:

            title = video.get(
                "title",
                "Untitled Video"
            )

            channel = video.get(
                "channel",
                ""
            )

            url = video.get(
                "url",
                ""
            )


            if url:

                if channel:

                    st.markdown(
                        f"- [{title}]({url}) "
                        f"— {channel}"
                    )

                else:

                    st.markdown(
                        f"- [{title}]({url})"
                    )

    else:

        st.info(
            "No YouTube videos were returned."
        )


    # ==================================================
    # Quality Control
    # ==================================================

    st.divider()

    st.header(
        "Quality Control Reports"
    )

    qc_reports = result.get(
        "qc_reports",
        {}
    )


    # ==================================================
    # QC 1 — Factual Accuracy
    # ==================================================

    with st.expander(
        "QC Layer 1 — Research & Factual Accuracy",
        expanded=True
    ):

        qc1 = qc_reports.get(
            "factual_accuracy",
            {}
        )


        if qc1:

            if "content" in qc1:

                parts = qc1["content"].get(
                    "parts",
                    []
                )


                if parts:

                    qc1_text = parts[0].get(
                        "text",
                        ""
                    )

                    st.markdown(
                        qc1_text
                    )

                else:

                    st.json(
                        qc1
                    )

            else:

                st.json(
                    qc1
                )

        else:

            st.info(
                "QC Layer 1 report was not returned."
            )


    # ==================================================
    # QC 2 — Instructional Quality
    # ==================================================

    with st.expander(
        "QC Layer 2 — Instructional Quality",
        expanded=True
    ):

        qc2 = qc_reports.get(
            "instructional_quality",
            {}
        )


        if qc2:

            if "content" in qc2:

                parts = qc2["content"].get(
                    "parts",
                    []
                )


                if parts:

                    qc2_text = parts[0].get(
                        "text",
                        ""
                    )

                    st.markdown(
                        qc2_text
                    )

                else:

                    st.json(
                        qc2
                    )

            else:

                st.json(
                    qc2
                )

        else:

            st.info(
                "QC Layer 2 report was not returned."
            )


    # ==================================================
    # Export
    # ==================================================

    st.divider()

    st.header("Export Final Lesson")

    # --------------------------------------------------
    # Determine final lesson
    # --------------------------------------------------

    if st.session_state["edited_lesson"]:

        final_lesson = st.session_state[
            "edited_lesson"
        ]

    else:

        final_lesson = lesson_text


    # --------------------------------------------------
    # Extract QC text for export
    # --------------------------------------------------

    qc1_export = ""

    if "content" in qc_reports.get(
        "factual_accuracy",
        {}
    ):

        parts = qc_reports[
            "factual_accuracy"
        ]["content"].get(
            "parts",
            []
        )

        if parts:

            qc1_export = parts[0].get(
                "text",
                ""
            )


    qc2_export = ""

    if "content" in qc_reports.get(
        "instructional_quality",
        {}
    ):

        parts = qc_reports[
            "instructional_quality"
        ]["content"].get(
            "parts",
            []
        )

        if parts:

            qc2_export = parts[0].get(
                "text",
                ""
            )


    # ==================================================
    # Markdown lesson export
    # ==================================================

    final_lesson_file = final_lesson


    # ==================================================
    # Complete lesson report
    # ==================================================

    report_lines = []

    report_lines.append(
        f"# {result.get('lesson_title', '')}"
    )

    report_lines.append("")

    report_lines.append(
        "## Learning Objective"
    )

    report_lines.append("")

    report_lines.append(
        result.get(
            "learning_objective",
            ""
        )
    )

    report_lines.append("")

    report_lines.append(
        "## Final Lesson"
    )

    report_lines.append("")

    report_lines.append(
        final_lesson
    )

    report_lines.append("")

    report_lines.append(
        "## Web References"
    )

    report_lines.append("")


    for source in web_sources:

        title = source.get(
            "title",
            "Untitled Source"
        )

        url = source.get(
            "url",
            ""
        )

        if url:

            report_lines.append(
                f"- [{title}]({url})"
            )


    report_lines.append("")

    report_lines.append(
        "## Book References"
    )

    report_lines.append("")


    for book in book_sources:

        title = book.get(
            "title",
            "Untitled Book"
        )

        authors = book.get(
            "authors",
            []
        )

        url = book.get(
            "url",
            ""
        )


        if isinstance(
            authors,
            list
        ):

            author_text = ", ".join(
                authors
            )

        else:

            author_text = str(
                authors
            )


        if url:

            report_lines.append(
                f"- [{title}]({url})"
                f" — {author_text}"
            )

        else:

            report_lines.append(
                f"- {title} — {author_text}"
            )


    report_lines.append("")

    report_lines.append(
        "## YouTube References"
    )

    report_lines.append("")


    for video in youtube_videos:

        title = video.get(
            "title",
            "Untitled Video"
        )

        channel = video.get(
            "channel",
            ""
        )

        url = video.get(
            "url",
            ""
        )


        if url:

            report_lines.append(
                f"- [{title}]({url}) — {channel}"
            )


    report_lines.append("")

    report_lines.append(
        "## QC Layer 1 — Research & Factual Accuracy"
    )

    report_lines.append("")

    report_lines.append(
        qc1_export
    )

    report_lines.append("")

    report_lines.append(
        "## QC Layer 2 — Instructional Quality"
    )

    report_lines.append("")

    report_lines.append(
        qc2_export
    )


    lesson_report = "\n".join(
        report_lines
    )


    # ==================================================
    # Complete JSON export
    # ==================================================

    export_data = {
        "lesson_title": result.get(
            "lesson_title",
            ""
        ),

        "learning_objective": result.get(
            "learning_objective",
            ""
        ),

        "final_lesson": final_lesson,

        "research": research,

        "qc_reports": qc_reports
    }


    project_json = json.dumps(
        export_data,
        indent=2,
        ensure_ascii=False
    )


    # ==================================================
    # Download buttons
    # ==================================================

    st.subheader("Download Files")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.download_button(
            label="Download Final Lesson",
            data=final_lesson_file,
            file_name="final_lesson.md",
            mime="text/markdown"
        )


    with col2:

        st.download_button(
            label="Download Lesson Report",
            data=lesson_report,
            file_name="lesson_report.md",
            mime="text/markdown"
        )


    with col3:

        st.download_button(
            label="Download Project Data",
            data=project_json,
            file_name="lesson_project.json",
            mime="application/json"
        )