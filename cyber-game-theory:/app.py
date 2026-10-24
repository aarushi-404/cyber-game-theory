import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from game_model import DEFAULT_ATTACKS, DEFAULT_DEFENSES, DEFAULT_PAYOFF, solve_zero_sum_game, pure_saddle_point

st.set_page_config(page_title="Cyber Game Theory Analytics", page_icon="🛡️", layout="wide")
st.title("Game-Theoretic Analysis of Cyber Attack and Defense Strategies")
st.caption("Educational simulator using hypothetical utility scores. No real attacks are performed.")
ACTIONS, CONTROLS = DEFAULT_ATTACKS, DEFAULT_DEFENSES
SCENARIOS = {
 "Baseline": np.array([[-2,4,1],[5,-3,2],[3,2,-4]],float),
 "Stronger phishing resistance": np.array([[-2,4,1],[5,-6,2],[3,2,-4]],float),
 "Enhanced monitoring": np.array([[-2,4,-2],[5,-3,-1],[3,2,-7]],float),
 "Layered defense": np.array([[-4,2,-1],[3,-6,0],[1,1,-7]],float),
 "Limited monitoring budget": np.array([[-2,4,3],[5,-3,4],[3,2,-1]],float),
 "Hardened web server": np.array([[-6,4,1],[5,-3,2],[3,2,-4]],float)
}
st.sidebar.header("Scenario controls")
scenario=st.sidebar.selectbox("Select scenario",list(SCENARIOS))
matrix=SCENARIOS[scenario].copy()
if st.sidebar.toggle("Edit payoff values",False):
    for i,a in enumerate(ACTIONS):
        with st.sidebar.expander(a):
            for j,c in enumerate(CONTROLS):
                matrix[i,j]=st.number_input(c,-20.0,20.0,float(matrix[i,j]),1.0,key=f"{scenario}_{i}_{j}")
sol=solve_zero_sum_game(matrix); pure=pure_saddle_point(matrix)
cols=st.columns(4)
for col,label,value in zip(cols,["Attacker actions","Defensive controls","Equilibrium utility","Pure saddle point"],[len(ACTIONS),len(CONTROLS),f"{sol['value']:.3f}","Yes" if pure else "No"]): col.metric(label,value)
overview,strategy,scenarios,sensitivity,method=st.tabs(["Overview","Strategy analysis","Scenario comparison","Sensitivity analysis","Method & assumptions"])
with overview:
    st.subheader(f"Payoff matrix — {scenario}")
    st.write("Each cell is a hypothetical attacker utility score, not a probability or measured loss.")
    st.dataframe(pd.DataFrame(matrix,index=ACTIONS,columns=CONTROLS).style.format("{:.1f}").background_gradient(cmap="RdYlBu_r",axis=None),use_container_width=True)
    fig,ax=plt.subplots(figsize=(7,4))
    im=ax.imshow(matrix,cmap="RdYlBu_r",aspect="auto")
    ax.set_xticks(range(len(CONTROLS)),CONTROLS,rotation=18,ha="right"); ax.set_yticks(range(len(ACTIONS)),ACTIONS)
    ax.set_title("Attacker utility heatmap")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]): ax.text(j,i,f"{matrix[i,j]:.1f}",ha="center",va="center",color="black")
    fig.colorbar(im,ax=ax,label="Attacker utility"); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    st.info(f"Pure saddle point: {ACTIONS[pure[0]]} vs {CONTROLS[pure[1]]}, value {pure[2]:.2f}" if pure else "No pure saddle point; mixed strategies are used.")
with strategy:
    st.subheader("Optimal mixed strategies")
    l,r=st.columns(2)
    for col,player,names,probs in [(l,"Attacker",ACTIONS,sol["p"]),(r,"Defender",CONTROLS,sol["q"])]:
        with col:
            st.markdown(f"**{player} strategy probabilities**")
            st.dataframe(pd.DataFrame({"Strategy":names,"Probability":probs,"Percent":probs*100}).style.format({"Probability":"{:.3f}","Percent":"{:.1f}%"}),hide_index=True,use_container_width=True)
            fig,ax=plt.subplots(figsize=(6,3)); ax.barh(names,probs); ax.set_xlim(0,1); ax.set_xlabel("Probability"); ax.set_title(f"{player} mix"); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    st.subheader("Expected payoff against each pure action")
    st.dataframe(pd.DataFrame({"Defender action":CONTROLS,"Expected attacker payoff":sol["p"]@matrix}).style.format({"Expected attacker payoff":"{:.3f}"}),hide_index=True,use_container_width=True)
    st.dataframe(pd.DataFrame({"Attacker action":ACTIONS,"Payoff against defender mix":matrix@sol["q"]}).style.format({"Payoff against defender mix":"{:.3f}"}),hide_index=True,use_container_width=True)
with scenarios:
    st.subheader("Six-scenario comparison")
    rows=[]
    for name,mat in SCENARIOS.items():
        result=solve_zero_sum_game(mat); p,q=result["p"],result["q"]
        hp=float(-np.sum(p[p>0]*np.log2(p[p>0]))); hq=float(-np.sum(q[q>0]*np.log2(q[q>0])))
        rows.append({"Scenario":name,"Equilibrium utility":result["value"],"Attacker strategy entropy":hp,"Defender strategy entropy":hq})
    comp=pd.DataFrame(rows).sort_values("Equilibrium utility")
    st.dataframe(comp.style.format({"Equilibrium utility":"{:.3f}","Attacker strategy entropy":"{:.3f}","Defender strategy entropy":"{:.3f}"}),hide_index=True,use_container_width=True)
    fig,ax=plt.subplots(figsize=(9,4)); ax.barh(comp["Scenario"],comp["Equilibrium utility"]); ax.axvline(0,color="black",linewidth=.8); ax.set_xlabel("Equilibrium attacker utility (lower favors defender)"); ax.set_title("Illustrative scenario comparison"); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    st.info(f"Lowest modeled attacker utility: {comp.iloc[0]['Scenario']} ({comp.iloc[0]['Equilibrium utility']:.3f}). This is true only for the assumed utility matrices.")
with sensitivity:
    st.subheader("Sensitivity analysis")
    st.write("Change one payoff cell and observe how the equilibrium changes.")
    attack=st.selectbox("Attack row",ACTIONS,index=1); control=st.selectbox("Defense column",CONTROLS,index=1); extent=st.slider("Adjustment range",1,10,5)
    i,j=ACTIONS.index(attack),CONTROLS.index(control); rows=[]
    for delta in range(-extent,extent+1):
        temp=matrix.copy(); temp[i,j]+=delta; result=solve_zero_sum_game(temp)
        row={"Adjustment":delta,"Changed utility":temp[i,j],"Equilibrium utility":result["value"]}
        row.update({f"Attacker P: {ACTIONS[k]}":result["p"][k] for k in range(len(ACTIONS))})
        row.update({f"Defender P: {CONTROLS[k]}":result["q"][k] for k in range(len(CONTROLS))}); rows.append(row)
    data=pd.DataFrame(rows)
    st.dataframe(data.style.format({c:"{:.3f}" for c in data.columns if c!="Adjustment"}),hide_index=True,use_container_width=True)
    fig,ax=plt.subplots(figsize=(9,4)); ax.plot(data["Adjustment"],data["Equilibrium utility"],marker="o"); ax.axvline(0,linestyle="--",linewidth=.8); ax.set_xlabel("Adjustment to selected payoff"); ax.set_ylabel("Equilibrium utility"); ax.set_title(f"Sensitivity: {attack} × {control}"); ax.grid(True,alpha=.25); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    st.download_button("Download sensitivity CSV",data.to_csv(index=False).encode(),file_name="sensitivity_analysis.csv",mime="text/csv")
with method:
    st.markdown("""
**Players:** attacker maximizes utility; defender minimizes attacker utility.  
**Expected payoff:** `E(p, q) = pᵀ A q`  
**Solver:** linear programming returns optimal mixed strategies and game value.  
**Assumptions:** zero-sum preferences, rational players and a known payoff matrix.  
**Limitations:** utilities are illustrative—not probabilities, financial losses or empirical effectiveness. Real cyber defense includes uncertainty and incomplete information. This app does not scan networks or execute attacks.
""")
    st.download_button("Download current payoff matrix CSV",pd.DataFrame(matrix,index=ACTIONS,columns=CONTROLS).to_csv().encode(),file_name="current_payoff_matrix.csv",mime="text/csv")
st.caption("Python • NumPy • SciPy • Pandas • Matplotlib • Streamlit")
