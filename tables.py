import pandas as pd
import os
import plotly.express as px

def create_graph(file_name):
    try:
        path = os.path.join(os.path.dirname(__file__), 'uploads', file_name)
        print(f"Ruta del archivo CSV: {path}")
        if not os.path.exists(path):
            print("⚠️ El archivo no existe en la ruta:", path)
            return None, None, None

        df = pd.read_csv(path)
        expected_columns = {'Type', 'Product', 'Started Date', 'Completed Date', 'Description', 'Amount', 'Fee', 'Currency', 'State', 'Balance'}

        if not expected_columns.issubset(set(df.columns)):
            raise ValueError("El archivo CSV no tiene el formato correcto.")
        
        df["Type Amount"] = df["Amount"].apply(lambda x: "Expense" if x < 0 else "Income")
        df["Amount"] = df["Amount"].abs()
        max_val = df["Amount"].max()
        income = df.loc[df["Type Amount"] =="Income", ["Description","Amount","Type Amount"]]
        expense = df.loc[df["Type Amount"] == "Expense", ["Description","Amount","Type Amount"]]
    
        
        #Creando el gráfico de ingresos
        fig_income = px.bar(data_frame=income,x="Description", y="Amount", color="Type Amount",color_discrete_map={"Income":"#4CAF50"})
        fig_income.update_layout(
            title_font_size=24,
            title_x=0.5,  # Centrado
            plot_bgcolor="#F5F5F5",     # Fondo del gráfico
            paper_bgcolor="#FFFFFF",    # Fondo de todo el "papel"
            width = 800,
            font=dict(
                family="Arial, sans-serif", 
                size=14,
                color="#183B4E"          # Azul suave para textos
            ),
            xaxis=dict(
                title_font=dict(size=18),
                tickfont=dict(size=12),
                showgrid=False,          # Quitamos líneas verticales
                linecolor="#27548A", # Eje X en azul más oscuro
            ),
            yaxis=dict(
                range=[0, max_val],
                title_font=dict(size=18),
                tickfont=dict(size=12),
                showgrid=True,
                gridcolor="#E8DBC0",     # Color suave para líneas horizontales
                zerolinecolor="#DDA853"  # Línea de 0 en un dorado suave
            ),
            legend=dict(
                title=None,
                orientation="h",
                y=-0.2,
                x=0.5,
                xanchor="center",
                font=dict(size=12)
            ),
            margin=dict(l=40, r=40, t=80, b=80)  # Márgenes suaves
        )

        #Creando el gráfico de gastos
        fig_expense = px.bar(data_frame=expense,x="Description", y="Amount", color="Type Amount",color_discrete_map={"Expense":"#F44336"})
        fig_expense.update_layout(
            title_font_size=24,
            title_x=0.5,  # Centrado
            plot_bgcolor="#F5F5F5",     # Fondo del gráfico
            paper_bgcolor="#FFFFFF",    # Fondo de todo el "papel"
            width=800,
            font=dict(
                family="Arial, sans-serif", 
                size=14,
                color="#183B4E"          # Azul suave para textos
            ),
            xaxis=dict(
                title_font=dict(size=18),
                tickfont=dict(size=12),
                showgrid=False,          # Quitamos líneas verticales
                linecolor="#27548A"      # Eje X en azul más oscuro
            ),
            yaxis=dict(
                range=[0, max_val],
                title_font=dict(size=18),
                tickfont=dict(size=12),
                showgrid=True,
                gridcolor="#E8DBC0",     # Color suave para líneas horizontales
                zerolinecolor="#DDA853"  # Línea de 0 en un dorado suave
            ),
            legend=dict(
                title=None,
                orientation="h",
                y=-0.2,
                x=0.5,
                xanchor="center",
                font=dict(size=12)
            ),
            margin=dict(l=40, r=40, t=80, b=80)  # Márgenes suaves
        )

        #Concatenando ingresos y gastos para luego hacer el gráfico de comparativa
        concat = pd.concat([income,expense])
        fig_comparison = px.bar(data_frame=concat,x="Description", y="Amount", color="Type Amount",barmode="group",color_discrete_map={"Income":"#4CAF50","Expense":"#F44336"})
        fig_comparison.update_layout(
            title_font_size=24,
            title_x=0.5,  # Centrado
            plot_bgcolor="#F5F5F5",     # Fondo del gráfico
            paper_bgcolor="#FFFFFF",    # Fondo de todo el "papel"
            width=800,
            font=dict(
                family="Arial, sans-serif", 
                size=14,
                color="#183B4E"          # Azul suave para textos
            ),
            xaxis=dict(
                title_font=dict(size=18),
                tickfont=dict(size=12),
                showgrid=False,          # Quitamos líneas verticales
                linecolor="#27548A"      # Eje X en azul más oscuro
            ),
            yaxis=dict(
                range=[0, max_val],
                title_font=dict(size=18),
                tickfont=dict(size=12),
                showgrid=True,
                gridcolor="#E8DBC0",     # Color suave para líneas horizontales
                zerolinecolor="#DDA853"  # Línea de 0 en un dorado suave
            ),
            legend=dict(
                title=None,
                orientation="h",
                y=-0.2,
                x=0.5,
                xanchor="center",
                font=dict(size=12)
            ),
            margin=dict(l=40, r=40, t=80, b=80)  # Márgenes suaves
        )

        return (fig_income.to_html(full_html=False,include_plotlyjs='cdn', config={'responsive': True}),fig_expense.to_html(full_html=False,include_plotlyjs='cdn', config={'responsive': True}),fig_comparison.to_html(full_html=False,include_plotlyjs='cdn', config={'responsive': True}))

    except Exception as e:
        print(f"Error en create_graph: {e}")
        return None, None, None
