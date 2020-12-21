# -*- coding: utf-8 -*-

from yattag import Doc


def get_filename(language: str) -> str:
    """Generate a filename for the analyzer to fix the language to use."""
    if language == "python":
        return "test.py"
    return "test.c"


def setup_html(doc, tag) -> None:
    """Generate the HTML skeleton."""
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('link'):
                doc.attr(rel="stylesheet")
                doc.attr(href="/static/normalize.css")
            with tag('link'):
                doc.attr(rel="stylesheet")
                doc.attr(href="/static/skeleton.css")


def generate_analysis_results(analysis, code: str) -> str:
    """Pack the analysis results into a visual HTML table."""
    doc, tag, text = Doc().tagtext()
    setup_html(doc, tag)
    results_dict = analysis.__dict__
    functions_list = results_dict['function_list']

    with tag('body'):
        with tag('div'):
            doc.attr(klass="container")
            doc.attr(style="margin-top:2em;")
            with doc.tag('h2'):
                doc.text("Static Analysis Results")
            with doc.tag('pre'):
                with doc.tag('code'):
                    doc.text(code)
            with doc.tag('table'):
                doc.attr(klass="u-full-width")
                with doc.tag('tbody'):
                    with doc.tag('tr'):
                        with doc.tag('th'):
                            doc.text('Average Cyclomatic Complexity')
                        with doc.tag('td'):
                            doc.text(analysis.average_cyclomatic_complexity)
                    with doc.tag('tr'):
                        with doc.tag('th'):
                            doc.text('Lines of Code')
                        with doc.tag('td'):
                            doc.text(results_dict['nloc'])
                    with doc.tag('tr'):
                        with doc.tag('th'):
                            doc.text('Average Token Count')
                        with doc.tag('td'):
                            doc.text(results_dict['token_count'])
                    if functions_list:
                        for function in functions_list:
                            attr_to_print = (
                                ('cyclomatic_complexity', 'Cyclomatic Complexity'),
                                ('nloc', 'Lines of Code'),
                                ('parameter_count', 'Number of Parameters'),
                                ('length', 'Length'),
                                ('fan_in', 'Fan In'),
                                ('fan_out', 'Fan Out'),
                                ('top_nesting_level', 'Nesting Level'))
                            with doc.tag('tr'):
                                with doc.tag('th'):
                                    doc.attr(colspan="2")
                                    doc.attr(style="text-align:center;")
                                    doc.text('Function: {0}'.format(function.name))
                            for attr in attr_to_print:
                                with doc.tag('tr'):
                                    with doc.tag('th'):
                                        doc.text(attr[1])
                                    with doc.tag('td'):
                                        doc.text(getattr(function, attr[0]))
                    else:
                        with doc.tag('tr'):
                            with doc.tag('th'):
                                doc.text('Functions')
                            with doc.tag('td'):
                                doc.text('None')
    return doc.getvalue()

def generate_start_page() -> str:
    """Show the start form to submit to the analyzer."""
    doc, tag, text = Doc().tagtext()
    setup_html(doc, tag)
    with tag('body'):
        with tag('div'):
            doc.attr(klass="container")
            doc.attr(style="margin-top:2em;")
            with tag('h2'):
                text('Welcome to Code Finder')
            with tag('form', action="/analyseform"):
                doc.attr(method="POST")
                with tag('div'):
                    doc.attr(klass="row")
                    with doc.select(name="language"):
                        doc.attr(klass="u-full-width")
                        for value, desc in (
                                ('python', 'Python'),
                        ):
                            with doc.option(value=value):
                                text(desc)
                    with doc.tag('textarea', name="code"):
                        doc.attr(klass="u-full-width")
                        doc.attr(rows=8)
                    doc.stag('input', type="submit", value="Analyse", klass="button-primary")

    return doc.getvalue()
