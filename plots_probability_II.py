import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sps
import scipy.integrate as spint
# Freeze the parameters of the bivariate normal distribution: means and covariance matrix for x and y
bvn = sps.multivariate_normal([0.1, -0.2], [[0.3, 0.3], [0.3, 1.0]])
# Next we must set up a grid of x and y values to calculate the bivariate normal for, on each axis the
# grid ranges from -3 to 3, with step size 0.01
x, y = np.mgrid[-3:3:0.01, -3:3:0.01]
xypos = np.dstack((x, y))
# Calculate the bivariate joint pdf and for each variable marginalise (integrate) the joint pdf over the 
# other variable to obtain marginal pdfs for x and y
xypdf = bvn.pdf(xypos)
xpdf = spint.simpson(xypdf,y,axis=1)
ypdf = spint.simpson(xypdf,x,axis=0)
# Now define x and y ranges to calculate a 'slice' of the joint pdf, corresponding to the conditional pdfs
# for given x_0 and y_0
xrange = np.arange(-3,3,0.01)
yrange = np.arange(-3,3,0.01)
# We must create corresponding ranges of fixed x and y
xfix = np.full(len(yrange),0.7)
yfix = np.full(len(xrange),1.5)
# And define our arrays for the pdf to be calculated
xfix_pos = np.dstack((xfix, yrange))
yfix_pos = np.dstack((xrange, yfix))
# Now we calculate the conditional pdfs for each case, remembering to normalise by the integral of the 
# conditional pdf so the integrated probability = 1
bvny_xfix = bvn.pdf(xfix_pos)/spint.simpson(bvn.pdf(xfix_pos),yrange)
bvnx_yfix = bvn.pdf(yfix_pos)/spint.simpson(bvn.pdf(yfix_pos),xrange)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# Plot the marginal pdfs on the sides of the 3D box (corresponding to y=3 and x=-3)
ax.plot3D(x[:,0],np.full(len(xpdf),3.0),xpdf,color='black',label=r'$p(x)$')
ax.plot3D(np.full(len(ypdf),-3.0),y[0,:],ypdf,color='red',label=r'$p(y)$')
# Plot the slices through the joint pdf corresponding to the conditional pdfs:
ax.plot3D(xrange,yfix,bvn.pdf(yfix_pos),color='magenta',linewidth=2,label=r'$p(x,y=1.5)$')
ax.plot3D(xfix,yrange,bvn.pdf(xfix_pos),color='orange',linewidth=2,label=r'$p(x=0.7,y)$')
# Plot the normalised conditional pdf on the same box-sides as the marginal pdfs
ax.plot3D(xrange,np.full(len(xrange),3.0),bvnx_yfix,color='magenta',linestyle='dashed',label=r'$p(x\vert y=1.5)$')
ax.plot3D(np.full(len(yrange),-3.0),yrange,bvny_xfix,color='orange',linestyle='dashed',label=r'$p(y\vert x=0.7)$')
# Plot the joint pdf as a wireframe:
ax.plot_wireframe(x, y, xypdf, rstride=20, cstride=20, alpha=0.3, color='gray')
# Plot labels and the legend
ax.set_xlabel(r'$x$',fontsize=14)
ax.set_ylabel(r'$y$',fontsize=14)
ax.set_zlabel(r'probability density',fontsize=12)
ax.legend(fontsize=9,ncol=2)
plt.show()

# We set the figsize so that we get a square plot with x and y axes units having equal dimension 
# (so the contours are not artificially stretched)
fig = plt.figure(figsize=(6,6))
# Add a gridspec with two rows and two columns and a ratio of 3 to 7 between
# the size of the marginal axes and the main axes in both directions.
# We also adjust the subplot parameters to obtain a square plot.
gs = fig.add_gridspec(2, 2,  width_ratios=(7, 3), height_ratios=(3, 7), left=0.1, right=0.9, 
                          bottom=0.1, top=0.9, wspace=0.03, hspace=0.03)
# Set up the subplots and their shared axes
ax = fig.add_subplot(gs[1, 0])
ax_xpdfs = fig.add_subplot(gs[0, 0], sharex=ax)
ax_ypdfs = fig.add_subplot(gs[1, 1], sharey=ax)
# Turn off the tickmark values where necessary
ax_xpdfs.tick_params(axis="x", labelbottom=False)
ax_ypdfs.tick_params(axis="y", labelleft=False)
con = ax.contour(x, y, xypdf)  # The contour plot
# Marginal and conditional pdfs plotted in the side/top panel
ax_xpdfs.plot(x[:,0],xpdf,color='black',label=r'$p(x)$')
ax_ypdfs.plot(ypdf,y[0,:],color='red',label=r'$p(y)$')
ax_xpdfs.plot(xrange,bvnx_yfix,color='magenta',linestyle='dashed',label=r'$p(x\vert y=1.5)$')
ax_ypdfs.plot(bvny_xfix,yrange,color='orange',linestyle='dashed',label=r'$p(y\vert x=0.7)$')
# Lines on the contour show the slices used for the conditional pdfs
ax.axhline(1.5,color='magenta',alpha=0.5)
ax.axvline(0.7,color='orange',alpha=0.5)
# Plot labels and legend
ax.set_xlabel(r'$x$',fontsize=14)
ax.set_ylabel(r'$y$',fontsize=14)
ax_xpdfs.set_ylabel(r'probability density',fontsize=12)
ax_ypdfs.set_xlabel(r'probability density',fontsize=12)
ax.clabel(con, inline=1, fontsize=8) # This adds labels to show the value of each contour level
ax_xpdfs.legend()
ax_ypdfs.legend()
#plt.savefig('2d_joint_prob.png',bbox_inches='tight')
plt.show()