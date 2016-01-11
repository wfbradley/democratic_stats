import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
from scipy.stats import beta
import seaborn as sns
import sys
import argparse


def plot_two_betas(a1=None,b1=None,label1=None,a2=None,b2=None,label2=None,num=10000,threshold=.001):
	x=np.linspace(1./float(num+1),1.0-1./float(num+1),num=num)
	y1=beta.pdf(x,a1,b1)
	big1=y1>=threshold
	plt.plot(100.0*x[big1],y1[big1],label=label1)
	if not (a2 is None):
		y2=beta.pdf(x,a2,b2)
		big2=y2>=threshold
		plt.plot(100.0*x[big2],y2[big2],label=label2)
	if not(label1 is None) or not(label2 is None):
		plt.legend(loc='best')
	plt.xlabel('Rate (in %)')
	plt.ylabel('Likelihood')

def plot_two_samples(a1=None,n1=None,label1='',a2=None,n2=None,label2='',num=10000,threshold=.001):

	b1=n1-a1
	if a1<0 or n1<a1:
		print "Must have 0<=a1<=n1"
		sys.exit(0)

	label1_extra='%d of %d (%.2f%%)'%(int(a1),int(n1),100.0*a1/n1)
	if label1 is '':
		label1=label1_extra
	else:
		label1+=' (%s)'%label1_extra


	b2=n2-a2
	# Must have a2 and n2 BOTH none or NEITHER none:
	if (a2 is np.nan) or (n2 is np.nan):
		if not ((a2 is np.nan) and (n2 is np.nan)):
			print "Need to set a2 AND n2, if using them."
			sys.exit(0)
	else:
		if a2<0 or n2<a2:
			print "Must have 0<=a2<=n2"
			sys.exit(0)
		b2=n2-a2

		label2_extra='%d of %d (%.2f%%)'%(int(a2),int(n2),100.0*a2/n2)
		if label2 is '':
			label2=label2_extra
		else:
			label2+=' (%s)'%label2_extra

	# Add uniform prior:
	a1+=1
	b1+=1
	a2+=1
	b2+=1

	plot_two_betas(a1=a1,b1=b1,a2=a2,b2=b2,label1=label1,label2=label2,threshold=threshold)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=
		'Comparing probability between two coins (posterior is beta given uniform prior).  Coin #2 and labels are optional.')
	parser.add_argument('--a1', type=float, required=True,
		help='Heads (coin #1)')
	parser.add_argument('--a2', type=float, default=np.nan,
		help='Heads (coin #2)')
	parser.add_argument('--n1', type=float, required=True,
		help='Total coin flips (coin #1)')
	parser.add_argument('--n2', type=float, default=np.nan,
		help='Total coin flips (coin #2)')
	parser.add_argument('--label1', type=str, default='',
		help='Label (coin #1)')
	parser.add_argument('--label2', type=str, default='',
		help='Label (coin #2)')
	parser.add_argument('--threshold', type=float, default=.001,
		help='Only graph probability values greater than threshold (to restrict x range)')
	args = parser.parse_args()


	num_x_axis_samples=10000
	plot_two_samples(a1=args.a1,n1=args.n1,label1=args.label1,a2=args.a2,n2=args.n2,label2=args.label2,num=num_x_axis_samples,threshold=args.threshold)
	plt.show()
