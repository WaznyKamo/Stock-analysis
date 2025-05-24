import streamlit as st
import plotly.graph_objects as go

def plot_multiple_y_axes(df, columns, title_prefix="Wykres"):
    if not columns:
        st.warning("Wybierz co najmniej jedną kolumnę.")
        return

    fig = go.Figure()
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'gray']

    for i, col in enumerate(columns):
        yaxis_name = f'y{i+1}'
        showaxis = (i > 0)
        axis_id = '' if i == 0 else str(i + 1)
        
        fig.add_trace(go.Scatter(
            x=df['Data'],
            y=df[col],
            name=col,
            yaxis=f'y{axis_id}',
            line=dict(color=colors[i % len(colors)])
        ))

        # Dodaj dodatkową oś Y jeśli potrzebna
        if showaxis:
            fig.update_layout(**{
                f'yaxis{axis_id}': dict(
                    title=col,
                    overlaying='y',
                    side='right',
                    position=1.0 - 0.05 * (i - 1),
                    showgrid=False
                )
            })

    # Oś X i pierwsza oś Y
    fig.update_layout(
        title=f"{title_prefix}: {', '.join(columns)}",
        xaxis=dict(title='Data'),
        yaxis=dict(title=columns[0]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
