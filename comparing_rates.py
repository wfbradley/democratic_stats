import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
from scipy.stats import beta
import seaborn as sns
import sys
import argparse


def plot_two_betas(a=None,b=None,label=None,num=600,threshold=.001):
    epsilon=min(0.1/(a+b),.000001)

    if False: # Use uniform points
        x=np.linspace(1./float(num+1),1.0-1./float(num+1),num=num)
    else: # intelligently sample around modes
        var_x=a*b/( np.square(a+b)*(a+b+1.0) )
        std_dev_x=np.sqrt(var_x)
        mode_x=(a-1.0)/(a+b-2.0)
        mm=max(0.0,mode_x-6.0*std_dev_x)
        MM=min(1.0,mode_x+6.0*std_dev_x)
        x=np.linspace(mm+epsilon,MM-epsilon,num=num)
    y=beta.pdf(x,a,b)
    big=y>=threshold
    plt.plot(100.0*x[big],y[big],label=label)
    if not(label is None):
        plt.legend(loc='best')
    plt.xlabel('Rate (in %)')
    plt.ylabel('Probability density')
    return((x,y))

def plot_event_likelihood(a=None,n=None,label='',num=600,threshold=.001):
    # In case a, etc are passed as strings instead of floats
    a=float(a)
    n=float(n)

    b=n-a
    if a<0 or n<a:
        print "Must have 0<=a<=n"
        sys.exit(0)

    label_extra='%d of %d (%.2f%%)'%(int(a),int(n),100.0*a/n)
    if label is '':
        label=label_extra
    else:
        label+=' (%s)'%label_extra
    # Add uniform prior:
    a+=1
    b+=1

    return(plot_two_betas(a=a,b=b,label=label,num=num,threshold=threshold))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        'Probability of underlying rate of events based on observations.  '
        'Can optionally specify observations for a second rate.')
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
    parser.add_argument('--plot_resolution', type=float, default=600,
        help='Resolution of plot (e.g. 600=high resolution, 10=low resolution)')
    args = parser.parse_args()

    # Plot first curve
    (x1,y1)=plot_event_likelihood(a=args.a1,n=args.n1,label=args.label1,
        num=args.plot_resolution,threshold=args.threshold)

    # If specified, plot second curve
    if (args.a2 is not np.nan) and (args.n2 is not np.nan):
        (x2,y2)=plot_event_likelihood(a=args.a2,n=args.n2,label=args.label2,
            num=args.plot_resolution,threshold=args.threshold)

        # Figure out probability that second rate is > first rate.
        prob_2_is_bigger=0.0
        prob_normalizer=0.0

        mean1=args.a1/args.n1
        mean2=args.a2/args.n2
        two_bigger=False
        bigger=1
        smaller=2
        if mean2 >= mean1:
            two_bigger=True
            print 'two_bigger',two_bigger
            bigger=2
            smaller=1

        prob_2_is_much_bigger=0.0
        much_bigger_threshold=np.abs((mean1-mean2)/2.0)
        print mean1, mean2, much_bigger_threshold
        for i in xrange(len(x2)):
            for j in xrange(len(x1)):
                p_ij=y2[i]*y1[j]
                if x2[i]>x1[j]:
                    prob_2_is_bigger+=p_ij
                if two_bigger:
                    #print 'x2[%d]=%f'%(i,x2[i])
                    #print '[%d,%d], x1=%f, x2=%f >? %f  [%f]'%(i,j,x1[j],x2[i],x1[j]+much_bigger_threshold,much_bigger_threshold)
                    #print x2[i],x1[j]+much_bigger_threshold,x1[j],much_bigger_threshold
                    if x2[i]>x1[j]+much_bigger_threshold:
                        prob_2_is_much_bigger+=p_ij
                else:
                    if x1[j]>x2[i]+much_bigger_threshold:
                        prob_2_is_much_bigger+=p_ij

                prob_normalizer+=p_ij
        print prob_2_is_bigger
        print prob_2_is_much_bigger
        print prob_normalizer
        prob_2_is_bigger/=prob_normalizer
        prob_2_is_much_bigger/=prob_normalizer
        print "There is a %.2f%% chance that Coin #2 is greater than Coin #1"%(
            100.0*prob_2_is_bigger)
        print "(so, a %.2f%% chance that Coin #1 is greater than or equal to Coin #1)."%(
            100.0*(1.0-prob_2_is_bigger))
        print "The probability that Coin #%d is greater than Coin #%d by at least %.3f%% is %.2f%%."%(
            bigger,smaller,100.0*much_bigger_threshold,100.0*prob_2_is_much_bigger)

    plt.show()
