import streamlit as st
import plotly.graph_objects as go

def plot_multiple_y_axes(df, columns, title_prefix="Wykres"):
    if not columns:
        st.warning("Wybierz co najmniej jedną kolumnę.")
        return

    fig = go.Figure()
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'gray', 'cyan', 'magenta']

    # Rezerwujemy przestrzeń od 0.8 do 1.0 na dodatkowe osie Y po prawej
    min_position = 0.85
    max_position = 1.0
    num_additional_axes = len(columns) - 1

    step = (max_position - min_position) / max(num_additional_axes, 1) if num_additional_axes > 0 else 0

    for i, col in enumerate(columns):
        axis_suffix = '' if i == 0 else str(i + 1)
        yaxis_name = f'yaxis{axis_suffix}'
        yaxis_ref = f'y{axis_suffix}'

        fig.add_trace(go.Scatter(
            x=df['Data'],
            y=df[col],
            name=col,
            yaxis=yaxis_ref,
            xaxis='x',  # Wszystkie serie korzystają z tej samej osi X
            line=dict(color=colors[i % len(colors)])
        ))

        if i > 0:
            position = min_position + step * (i - 1)
            fig.update_layout(**{
                yaxis_name: dict(
                    title=None,  # <-- Ukryj tytuł osi Y
                    overlaying='y',
                    side='right',
                    position=round(position, 3),
                    showgrid=False,
                    tickfont=dict(color=colors[i % len(colors)])
                )
            })

    # Konfiguracja głównej osi Y i osi X
    fig.update_layout(
        title=f"{title_prefix}: {', '.join(columns)}",
        xaxis=dict(
            title='Data',
            tickfont=dict(size=10),
            domain=[0.0, 0.85],  # Os X zajmuje do 80% szerokości wykresu
        ),
        yaxis=dict(
            title=None,  # <-- Ukryj tytuł osi Y
            tickfont=dict(color=colors[0])
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=60, r=0, t=80, b=100),  # Więcej miejsca po prawej na osie Y
        width=1400,  # <-- ZWIĘKSZ SZEROKOŚĆ WYKRESU
        height=700   # <-- ZWIĘKSZ WYSOKOŚĆ WYKRESU
    )

    st.plotly_chart(fig, use_container_width=True)
