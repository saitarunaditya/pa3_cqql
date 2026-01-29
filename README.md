<h1>CQQL Query Engine</h1>
<h3>Practical Assignment 3 – Logic in Databases</h3>
<h4>BTU Cottbus–Senftenberg</h4>

<hr>

<h2>1. Project Description</h2>
<p>
This project implements a <strong>CQQL (Constraint and Query-based Query Language) engine</strong> in Python.
The engine processes logical queries that combine hard constraints, soft preferences, and weighted operators.
The system is <strong>dataset-independent</strong>: the same query can be evaluated on any object collection.
</p>

<h2>2. Features</h2>
<ul>
    <li>Parsing of CQQL expressions</li>
    <li>Support for NOT, AND, OR</li>
    <li>Weighted operators (WAND, WOR)</li>
    <li>Normalization into CQQL normal form</li>
    <li>Fuzzy evaluation and ranking</li>
    <li>Cross-platform console application</li>
</ul>

<h2>3. Folder Structure</h2>
<pre>
pa3_cqql/
│
├── main.py
├── cqql/
│   ├── ast.py
│   ├── parser.py
│   ├── weighting.py
│   ├── normalization.py
│   ├── evaluation.py
│   └── demo_data.py
│
└── README.html
</pre>

<h2>4. Installation</h2>
<p>Requirements:</p>
<ul>
    <li>Python 3.9+</li>
    <li>SymPy</li>
</ul>

<pre>pip install sympy</pre>

<h2>5. Running the Program</h2>
<pre>python main.py</pre>

<h2>6. Example Query</h2>
<pre>WAND(theta_text,theta_price,(quiet | modern),price__mid) & (pets | furnished)</pre>

<h2>7. Processing Pipeline</h2>
<ol>
    <li>Parse query</li>
    <li>Expand weighted operators</li>
    <li>Normalize formula</li>
    <li>Evaluate on dataset</li>
    <li>Rank results</li>
</ol>

<h2>8. Weighted Operators</h2>

<h3>WAND</h3>
<pre>WAND(t1,t2,A,B) → (A ∨ ¬t1) ∧ (B ∨ ¬t2)</pre>

<h3>WOR</h3>
<pre>WOR(t1,t2,A,B) → (A ∧ t1) ∨ (B ∧ t2)</pre>

<h2>9. Evaluation Semantics</h2>
<table border="1" cellpadding="6">
<tr><th>Operator</th><th>Rule</th></tr>
<tr><td>!φ</td><td>1 − φ</td></tr>
<tr><td>φ &amp; ψ</td><td>φ × ψ</td></tr>
<tr><td>φ | ψ</td><td>φ + ψ − φ×ψ</td></tr>
</table>

<p>
Database atoms return <strong>0 or 1</strong>.<br>
Text and proximity atoms return values in <strong>[0,1]</strong>.
</p>

<h2>10. Demo Dataset</h2>
<p>
The project includes a dataset of Berlin apartments with boolean, proximity,
and text-based attributes.
</p>
<h2>11. Sample CQQL Queries</h2>
<p>The following queries demonstrate the supported syntax and increasing complexity.</p>

<h3>Basic Queries</h3>
<pre>
Q1: balcony
Q2: quiet | modern
Q3: price__low & dist__near
</pre>

<h3>Weighted and Combined Queries</h3>
<pre>
Q4: WOR(theta_price,theta_dist, price__low, dist__near) & (balcony | elevator)

Q5: (price__low & kreuzberg) | (price__high & charlottenburg)

Q6: WAND(theta_text,theta_price, (quiet | modern), price__mid) & (pets | furnished)

Q7: WOR(theta_text,theta_text, quiet, modern) & size__large

Q8: WAND(theta_price,theta_dist, price__low, dist__near) & pets

Q9: (dist__near & quiet) | (dist__far & modern)

Q10: WOR(theta_text,theta_price, (quiet | modern), (price__low & dist__near)) & balcony
</pre>


<h2>12. Authors</h2>
<ul>
    <li>Sai Tharun Aditya, Kesana</li>
    <li>Salman</li>
    <li>Kaushik</li>
</ul>

</body>
</html>
