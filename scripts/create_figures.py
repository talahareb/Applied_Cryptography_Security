"""Generate README graphics (matplotlib is an optional plotting dependency)."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
OUT = Path('docs/images')
OUT.mkdir(parents=True,exist_ok=True)

fig,ax=plt.subplots(figsize=(11,3.4))
ax.set_axis_off()
ax.set_xlim(0,1);ax.set_ylim(0,1)
cols=['#eef4fc','#eaf7f5','#f6effb']
blocks=[('ENCRYPTION +\nKEY EXCHANGE','RSA-OAEP · AES-CTR / AES-GCM\nFinite-field DH · HKDF'),('HASHES +\nSIGNATURES','SHA-256 collision experiments\nToy Schnorr nonce analysis'),('TLS +\nCERTIFICATES','X.509 self-signed certificates\nLocal HTTPS client / server')]
for i,(title,body) in enumerate(blocks):
    x=0.02+i*.333
    p=plt.Rectangle((x,.24),.30,.59,facecolor=cols[i],edgecolor='#7892ae',lw=1.4,joinstyle='round')
    ax.add_patch(p)
    ax.text(x+.15,.68,title,ha='center',va='center',fontsize=10,fontweight='bold',color='#243955',linespacing=1.45)
    ax.text(x+.15,.44,body,ha='center',va='center',fontsize=8.4,color='#344256',linespacing=1.7)
    if i<2:ax.annotate('',(x+.324,.53),(x+.301,.53),arrowprops=dict(arrowstyle='->',lw=2,color='#52697e'))
fig.savefig(OUT/'cryptography_overview.png',dpi=180,bbox_inches='tight',facecolor='white');plt.close(fig)

# Recorded course measurements from the user's Lab 04 report, not rebenchmarked here.
bytes_count=np.array([1,2,3,4])
sha_first=[17.6,418.0,4350.0,44356.9]
sha_second=[17.4,138.4,3356.8,29443.0]
ideal=[2**(4*b) for b in bytes_count]
fig,ax=plt.subplots(figsize=(8.5,4.9))
ax.plot(bytes_count,ideal,color='#95a5b4',ls='--',marker='o',label='Birthday-order reference $2^{n/2}$')
ax.plot(bytes_count,sha_first,color='#276cad',marker='o',label='Recorded SHA-256 (C1)')
ax.plot(bytes_count,sha_second,color='#1d9e90',marker='s',label='Recorded SHA-256 (C2)')
ax.set_yscale('log');ax.set_xticks(bytes_count);ax.set_xlabel('Truncated digest length (bytes)')
ax.set_ylabel('Trials (log scale)');ax.set_title('Hash-collision complexity | Course observations')
ax.grid(alpha=.18);ax.legend(fontsize=9,loc='upper left')
fig.text(.125,.02,'Values transcribed from the 2025 Lab 04 report; not independently rerun.',fontsize=8,color='#536171')
fig.tight_layout(rect=[0,.05,1,1]);fig.savefig(OUT/'hash_collision_experiment.png',dpi=180,bbox_inches='tight',facecolor='white');plt.close(fig)
print('Wrote diagrams to',OUT)
