# app.py


import os
from flask import Flask, render_template, request, url_for
from agents.langgraph_pipeline import graph
from agents.langchain_pipeline import chain
from agents.image_agent import generate_image
from utils.exporter import save_as_markdown, save_as_pdf


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")
        content_type = request.form.get("content_type")
        tone = request.form.get("tone")
        pipeline = request.form.get("pipeline") # pipeline toggle



        combined_topic = f"{topic} ({content_type})"

    # Toggle between langGraph and classic chain
        if pipeline == "chain":
            result = chain.invoke({
                "topic": combined_topic,
                "tone": tone
            })
        else:
            result = graph.invoke({
                "topic": combined_topic,
                "tone": tone
            })

        final_content = result["final"]
        seo_keywords = result["keywords"]


        image_url = generate_image(topic)


        md_filename = save_as_markdown(final_content, topic)
        pdf_filename = save_as_pdf(final_content, topic)

        md_link = url_for("static", filename=f"exports/{md_filename}")
        pdf_link = url_for("static", filename=f"exports/{pdf_filename}")

        return render_template(
            "index.html",
            topic=topic,
            content_type=content_type,
            tone=tone,
            pipeline=pipeline,
            content=final_content,
            seo_keywords=seo_keywords,
            image_url=image_url,
            md_link=md_link,
            pdf_link=pdf_link
        )
    
    return render_template("index.html", topic=None)


if __name__ == "__main__":
    app.run(debug=True)
    

