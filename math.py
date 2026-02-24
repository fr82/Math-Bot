import matplotlib.pyplot as plt
import math
import re
import random
import io
import os
import discord
from discord.ext import commands, tasks 
from discord import Embed, ui, app_commands

guild_id = #serveridhere
bottoken = "bottokenhere"


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def gen_problem():
    """
    Gnerates our integral
    """

    problem_type = random.choice(["substitution", "by_parts", "trig", "partial_fractions", "exp_trig"])

    if problem_type == "substitution": # generates a by substitution problem
        # integral (2x)/(x^2 + a)^n dx
        a = random.choice([1, 2, 3, 4, 5, 7, 9])
        n = random.choice([1, 2, 3])
        q = rf"\int \frac{{2x}}{{(x^2+{a})^{n}}}\,dx"
        # Let u = x^2 + a => du = 2x dx
        if n == 1:
            ans = rf"\ln(x^2+{a}) + C"
            sol = rf"""
\textbf{{Let }} u=x^2+{a}\Rightarrow du=2x\,dx.\\
\int \frac{{2x}}{{(x^2+{a})}}dx=\int \frac{{1}}{{u}}du=\ln|u|+C=\ln(x^2+{a})+C.
"""
        else:
            # integral u^{-n} du = u^{1-n}/(1-n)
            ans = rf"\frac{{(x^2+{a})^{{1-{n}}}}}{{1-{n}}} + C"
            sol = rf"""
\textbf{{Let }} u=x^2+{a}\Rightarrow du=2x\,dx.\\
\int \frac{{2x}}{{(x^2+{a})^{n}}}dx=\int u^{{-{n}}}\,du
= \frac{{u^{{1-{n}}}}}{{1-{n}}}+C
= \frac{{(x^2+{a})^{{1-{n}}}}}{{1-{n}}}+C.
"""
        return q, sol.strip(), rf"\boxed{{{ans}}}"

    if problem_type == "by_parts": # generates a by parts problem
        # Integral x e^{kx} dx
        k = random.choice([1, 2, 3, -1, -2])
        q = rf"\int x e^{{{k}x}}\,dx"
        # Answer: e^{kx}(x/k - 1/k^2) + C
        ans = rf"e^{{{k}x}}\left(\frac{{x}}{{{k}}}-\frac{{1}}{{{k}^2}}\right)+C"
        sol = rf"""
\textbf{{Use integration by parts: }} \int u\,dv = uv-\int v\,du.\\
Let\; u=x\Rightarrow du=dx,\quad dv=e^{{{k}x}}dx\Rightarrow v=\frac{{1}}{{{k}}}e^{{{k}x}}.\\[4pt]
\int x e^{{{k}x}}dx = x\cdot\frac{{1}}{{{k}}}e^{{{k}x}}-\int \frac{{1}}{{{k}}}e^{{{k}x}}dx
= \frac{{x}}{{{k}}}e^{{{k}x}}-\frac{{1}}{{{k}^2}}e^{{{k}x}}+C.\\
= e^{{{k}x}}\left(\frac{{x}}{{{k}}}-\frac{{1}}{{{k}^2}}\right)+C.
"""
        return q, sol.strip(), rf"\boxed{{{ans}}}"

    if problem_type == "trig":
        # integral sin(ax) cos(ax) dx or ∫ sec^2(ax) dx, etc.
        a = random.choice([2, 3, 4, 5])
        variant = random.choice(["sin_cos", "sec2"])
        if variant == "sin_cos":
            q = rf"\int \sin({a}x)\cos({a}x)\,dx"
            ans = rf"\frac{{\sin^2({a}x)}}{{2{a}}}+C"
            sol = rf"""
\textbf{{Use substitution.}} Let\; u=\sin({a}x)\Rightarrow du={a}\cos({a}x)\,dx.\\
\int \sin({a}x)\cos({a}x)\,dx
= \frac{{1}}{{{a}}}\int u\,du
= \frac{{1}}{{{a}}}\cdot\frac{{u^2}}{{2}}+C
= \frac{{\sin^2({a}x)}}{{2{a}}}+C.
"""
            return q, sol.strip(), rf"\boxed{{{ans}}}"
        else:
            q = rf"\int \sec^2({a}x)\,dx"
            ans = rf"\frac{{1}}{{{a}}}\tan({a}x)+C"
            sol = rf"""
\textbf{{Recall:}} \frac{{d}}{{dx}}\tan({a}x) = {a}\sec^2({a}x).\\
So\; \int \sec^2({a}x)\,dx=\frac{{1}}{{{a}}}\tan({a}x)+C.
"""
            return q, sol.strip(), rf"\boxed{{{ans}}}"

    if problem_type == "partial_fractions":
        # integral (Ax + B)/(x^2 - p^2) dx  -> split into 1/(x-p), 1/(x+p)
        p = random.choice([2, 3, 4, 5])
        # Choose a simple numerator
        # We'll do INTEGRAL (2x)/(x^2 - p^2) dx = ln|x^2 - p^2| + C
        q = rf"\int \frac{{2x}}{{x^2-{p}^2}}\,dx"
        ans = rf"\ln|x^2-{p}^2|+C"
        sol = rf"""
\textbf{{Let }} u=x^2-{p}^2\Rightarrow du=2x\,dx.\\
\int \frac{{2x}}{{x^2-{p}^2}}dx=\int \frac{{1}}{{u}}du=\ln|u|+C=\ln|x^2-{p}^2|+C.
"""
        return q, sol.strip(), rf"\boxed{{{ans}}}"

    # exp_trig
    # INTEGRAL e^{ax} cos(bx) dx
    a = random.choice([1, 2])
    b = random.choice([2, 3])
    ax = "x" if a == 1 else f"{a}x"
    a_cos = rf"\cos({b}x)" if a == 1 else rf"{a}\cos({b}x)"
    q = rf"\int e^{{{ax}}}\cos({b}x)\,dx"
    # Standard result = e^{ax}cos(bx) dx = e^{ax}(a cos bx + b sin bx)/(a^2 + b^2) + C
    ans = rf"\frac{{e^{{{ax}}}\left({a_cos}+{b}\sin({b}x)\right)}}{{{a*a + b*b}}}+C"
    sol = rf"""
\textbf{{Use the standard result (or repeated integration by parts):}}\\
\int e^{{ax}}\cos(bx)\,dx = \frac{{e^{{ax}}\left(a\cos(bx)+b\sin(bx)\right)}}{{a^2+b^2}}+C.\\
Here,\; a={a},\; b={b}\Rightarrow\\
\int e^{{{ax}}}\cos({b}x)\,dx
= \frac{{e^{{{ax}}}\left({a_cos}+{b}\sin({b}x)\right)}}{{{a*a + b*b}}}+C.
"""
    return q, sol.strip(), rf"\boxed{{{ans}}}"

def render_latex_png(lines: list[str], title: str = "", fontsize: int = 18) -> discord.File:
    """
    Renders text into png
    """
    expanded_lines = []
    for line in lines:
        for part in str(line).splitlines():
            cleaned = part.strip()
            if cleaned:
                expanded_lines.append(cleaned)

    fig_h = max(4.5, 0.9 * len(expanded_lines) + (1.2 if title else 0.0))
    fig = plt.figure(figsize=(10, fig_h), dpi=200)
    ax = fig.add_subplot(111)
    ax.axis("off")

    def _clean_mathtext(s: str) -> str:
        s = s.replace(r"\,", " ").replace(r"\;", " ")
        s = s.replace(r"\Rightarrow", "=>")
        s = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", s)
        s = re.sub(r"\\text\{([^{}]*)\}", r"\1", s)
        if s.startswith(r"\boxed{") and s.endswith("}"):
            s = s[len(r"\boxed{"):-1]
        s = re.sub(r"\s+", " ", s)
        return s.strip()

    prepared_lines = []
    for line in expanded_lines:
        safe_line = _clean_mathtext(line)
        is_math = any(
            tok in safe_line
            for tok in (
                r"\int", r"\frac", r"\sin", r"\cos", r"\tan", r"\ln", r"\sec",
                r"\sqrt", "^", "_", r"\cdot", r"\left", r"\right"
            )
        )
        prepared_lines.append((safe_line, is_math))

    x = 0.02
    y = 0.96

    if title:
        title_obj = ax.text(
            x,
            y,
            title,
            fontsize=fontsize + 2,
            fontweight="bold",
            va="top",
            transform=ax.transAxes,
        )
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        title_h_axes = title_obj.get_window_extent(renderer=renderer).height / ax.bbox.height
        y -= title_h_axes + 0.05

    for safe_line, is_math in prepared_lines:
        text_value = f"${safe_line}$" if is_math else safe_line
        text_obj = ax.text(x, y, text_value, fontsize=fontsize, va="top", transform=ax.transAxes)

        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        line_h_axes = text_obj.get_window_extent(renderer=renderer).height / ax.bbox.height
        y -= line_h_axes + (0.03 if is_math else 0.02)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return discord.File(buf, filename="image.png")

class SolutionView(discord.ui.View):
    def __init__(self, question_png: discord.File, solution_png: discord.File):
        super().__init__(timeout=300)  # 5 min
        self.question_png = question_png
        self.solution_png = solution_png
        self.showing_solution = False

    @discord.ui.button(label="Show Solution", style=discord.ButtonStyle.primary)
    async def show_solution(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.showing_solution = True
        button.disabled = True
        button.label = "Solution Shown"

        embed = discord.Embed(title="Integral — Solution", color=discord.Color.green())
        embed.set_image(url="attachment://image.png")

        await interaction.response.edit_message(
            embed=embed,
            attachments=[self.solution_png],
            view=self
        )

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


@tree.command(
    name="integral",
    description="Generates an integral for you to solve.",
    guild=discord.Object(id=guild_id)
)
async def integral(interaction: discord.Interaction):
    q_latex, sol_steps, ans_latex = gen_problem()
    q_file = render_latex_png(
        lines=["Evaluate:", q_latex],
        title="Integration Practice — Question",
        fontsize=18
    )

    sol_lines = [
        "Worked solution:",
    ]
    # line split for display (keeps it simple)
    for raw in sol_steps.replace("\\\\", "\n").splitlines():
        s = raw.strip()
        if s:
            sol_lines.append(s)
    sol_lines.append("Final answer:")
    sol_lines.append(ans_latex)

    sol_file = render_latex_png(
        lines=sol_lines,
        title="Integration Practice — Solution",
        fontsize=14
    )

    embed = discord.Embed(title="Integral Question", color=discord.Color.blurple())
    embed.set_image(url="attachment://image.png")

    view = SolutionView(question_png=q_file, solution_png=sol_file)

    await interaction.response.send_message(
        embed=embed,
        file=q_file,
        view=view
    )

     
    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print(f"Logged in as {client.user}")



client.run(f"{bottoken}")