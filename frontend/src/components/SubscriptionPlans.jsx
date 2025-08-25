import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Check, Crown, Star, Zap, Users, Globe, TrendingUp } from 'lucide-react';

export default function SubscriptionPlans() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedBilling, setSelectedBilling] = useState('monthly');
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/subscription-plans`);
        if (response.ok) {
          const data = await response.json();
          setPlans(data.plans || []);
        }
        
        // Get current user info
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        setCurrentUser(user);
      } catch (error) {
        console.error('Error fetching plans:', error);
        // Fallback plans
        setPlans([
          {
            tier: 'starter',
            name: 'Starter',
            tagline: 'Perfect for small businesses getting started',
            monthly_price: 29,
            annual_price: 290,
            annual_savings: 58,
            highlights: ['1,000 Contacts', '3 Websites', '5 Funnels'],
            is_popular: false
          },
          {
            tier: 'professional',
            name: 'Professional',
            tagline: 'Ideal for growing businesses and agencies',
            monthly_price: 99,
            annual_price: 990,
            annual_savings: 198,
            highlights: ['10,000 Contacts', '25 Websites', '50 Funnels'],
            is_popular: true
          },
          {
            tier: 'white_label',
            name: 'White Label',
            tagline: 'Complete reseller solution',
            monthly_price: 2999,
            annual_price: 29990,
            annual_savings: 5998,
            highlights: ['Unlimited Everything', 'White-Label Solution', 'Reseller Program'],
            is_popular: false
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchPlans();
  }, []);

  const handleUpgrade = async (planTier) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/upgrade-subscription`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          plan_tier: planTier,
          billing_cycle: selectedBilling
        })
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message);
        
        if (data.next_steps?.checkout_url) {
          // In a real app, redirect to Stripe checkout
          console.log('Would redirect to:', data.next_steps.checkout_url);
        }
      } else {
        const error = await response.json();
        alert(error.error || 'Failed to upgrade subscription');
      }
    } catch (error) {
      console.error('Upgrade error:', error);
      alert('Failed to process upgrade request');
    }
  };

  const getPlanIcon = (tier) => {
    switch (tier) {
      case 'starter':
        return <Zap className="w-6 h-6" />;
      case 'professional':
        return <TrendingUp className="w-6 h-6" />;
      case 'business':
        return <Users className="w-6 h-6" />;
      case 'enterprise':
        return <Globe className="w-6 h-6" />;
      case 'white_label':
        return <Crown className="w-6 h-6" />;
      default:
        return <Star className="w-6 h-6" />;
    }
  };

  const getPlanColor = (tier) => {
    switch (tier) {
      case 'starter':
        return 'border-blue-200 bg-blue-50';
      case 'professional':
        return 'border-green-200 bg-green-50';
      case 'business':
        return 'border-purple-200 bg-purple-50';
      case 'enterprise':
        return 'border-orange-200 bg-orange-50';
      case 'white_label':
        return 'border-yellow-200 bg-gradient-to-br from-yellow-50 to-orange-50';
      default:
        return 'border-gray-200 bg-gray-50';
    }
  };

  const getButtonColor = (tier) => {
    switch (tier) {
      case 'starter':
        return 'bg-blue-600 hover:bg-blue-700';
      case 'professional':
        return 'bg-green-600 hover:bg-green-700';
      case 'business':
        return 'bg-purple-600 hover:bg-purple-700';
      case 'enterprise':
        return 'bg-orange-600 hover:bg-orange-700';
      case 'white_label':
        return 'bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700';
      default:
        return 'bg-gray-600 hover:bg-gray-700';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Choose Your Plan</h1>
        <p className="text-xl text-gray-600 mb-8">
          Scale your business with the ultimate all-in-one platform
        </p>
        
        {/* Billing Toggle */}
        <div className="inline-flex items-center bg-gray-100 rounded-lg p-1">
          <button
            onClick={() => setSelectedBilling('monthly')}
            className={`px-4 py-2 rounded-md font-medium transition-colors ${
              selectedBilling === 'monthly'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Monthly
          </button>
          <button
            onClick={() => setSelectedBilling('annually')}
            className={`px-4 py-2 rounded-md font-medium transition-colors ${
              selectedBilling === 'annually'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Annually
            <Badge className="ml-2 bg-green-100 text-green-800">Save 17%</Badge>
          </button>
        </div>
      </div>

      {/* Plans Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
        {plans.map((plan) => (
          <Card
            key={plan.tier}
            className={`relative ${getPlanColor(plan.tier)} ${
              plan.is_popular ? 'ring-2 ring-green-500 ring-offset-2 transform scale-105' : ''
            } transition-all hover:shadow-lg`}
          >
            {plan.is_popular && (
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <Badge className="bg-green-500 text-white px-3 py-1">Most Popular</Badge>
              </div>
            )}
            
            {plan.tier === 'white_label' && (
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <Badge className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white px-3 py-1">
                  <Crown className="w-3 h-3 mr-1" />
                  Premium
                </Badge>
              </div>
            )}

            <CardHeader className="text-center pb-4">
              <div className="flex justify-center mb-4">
                <div className={`p-3 rounded-full ${
                  plan.tier === 'white_label' 
                    ? 'bg-gradient-to-br from-yellow-100 to-orange-100 text-orange-600'
                    : plan.is_popular 
                    ? 'bg-green-100 text-green-600'
                    : 'bg-blue-100 text-blue-600'
                }`}>
                  {getPlanIcon(plan.tier)}
                </div>
              </div>
              
              <CardTitle className="text-2xl font-bold">{plan.name}</CardTitle>
              <CardDescription className="text-sm">{plan.tagline}</CardDescription>
              
              <div className="mt-4">
                <div className="flex items-baseline justify-center">
                  <span className="text-4xl font-bold">
                    ${selectedBilling === 'monthly' ? plan.monthly_price : plan.annual_price}
                  </span>
                  <span className="text-gray-600 ml-1">
                    /{selectedBilling === 'monthly' ? 'mo' : 'yr'}
                  </span>
                </div>
                
                {selectedBilling === 'annually' && plan.annual_savings > 0 && (
                  <div className="text-sm text-green-600 font-medium mt-1">
                    Save ${plan.annual_savings}/year
                  </div>
                )}
              </div>
            </CardHeader>

            <CardContent className="space-y-4">
              <div className="space-y-2">
                {(plan.highlights || []).map((feature, index) => (
                  <div key={index} className="flex items-center text-sm">
                    <Check className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                    <span>{feature}</span>
                  </div>
                ))}
              </div>

              <Button
                onClick={() => handleUpgrade(plan.tier)}
                className={`w-full ${getButtonColor(plan.tier)} text-white font-medium py-2 px-4 rounded-lg transition-all`}
                disabled={currentUser?.subscription_tier === plan.tier}
              >
                {currentUser?.subscription_tier === plan.tier ? 'Current Plan' : 
                 plan.tier === 'white_label' ? 'Become Reseller' : 'Upgrade Now'}
              </Button>

              {plan.tier === 'white_label' && (
                <div className="text-xs text-center text-gray-600 mt-2">
                  <p>Includes reseller program</p>
                  <p>30% commission on sub-accounts</p>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Features Comparison */}
      <div className="mt-16">
        <h2 className="text-2xl font-bold text-center mb-8">Feature Comparison</h2>
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-4 text-left font-medium text-gray-900">Features</th>
                  <th className="px-6 py-4 text-center font-medium text-gray-900">Starter</th>
                  <th className="px-6 py-4 text-center font-medium text-gray-900">Professional</th>
                  <th className="px-6 py-4 text-center font-medium text-gray-900">Business</th>
                  <th className="px-6 py-4 text-center font-medium text-gray-900">Enterprise</th>
                  <th className="px-6 py-4 text-center font-medium text-gray-900">White Label</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {[
                  ['Contacts', '1,000', '10,000', '100,000', '1,000,000', 'Unlimited'],
                  ['Websites', '3', '25', '100', '500', 'Unlimited'],
                  ['Marketing Funnels', '5', '50', '200', '1,000', 'Unlimited'],
                  ['AI Content/Month', '50', '500', '2,000', '10,000', 'Unlimited'],
                  ['Email Sends/Month', '2,000', '20,000', '100,000', '1,000,000', 'Unlimited'],
                  ['Team Members', '2', '10', '50', '200', 'Unlimited'],
                  ['Custom Domain', '❌', '✅', '✅', '✅', '✅'],
                  ['White-Label', '❌', '❌', '❌', '❌', '✅'],
                  ['Sub-Accounts', '❌', '❌', '❌', '❌', 'Unlimited'],
                  ['Priority Support', '❌', '✅', '✅', '✅', '✅'],
                  ['Phone Support', '❌', '❌', '✅', '✅', '✅'],
                  ['Reseller Program', '❌', '❌', '❌', '❌', '✅']
                ].map(([feature, ...values], index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                    <td className="px-6 py-4 font-medium text-gray-900">{feature}</td>
                    {values.map((value, valueIndex) => (
                      <td key={valueIndex} className="px-6 py-4 text-center text-sm text-gray-600">
                        {value}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* FAQ Section */}
      <div className="mt-16">
        <h2 className="text-2xl font-bold text-center mb-8">Frequently Asked Questions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="font-semibold mb-2">What makes the White Label tier special?</h3>
            <p className="text-gray-600 text-sm">
              The White Label tier is designed for agencies and resellers who want to offer 
              our platform to their clients under their own brand. You get unlimited access 
              to all features, can create unlimited sub-accounts, and earn 30% commission 
              on all sub-account subscriptions.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Can I upgrade or downgrade anytime?</h3>
            <p className="text-gray-600 text-sm">
              Yes! You can upgrade or downgrade your plan at any time. Changes take effect 
              immediately, and you'll be prorated for the difference.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Do you offer custom enterprise solutions?</h3>
            <p className="text-gray-600 text-sm">
              Absolutely! Our Enterprise and White Label tiers include custom integrations 
              and dedicated account management. Contact us for tailored solutions.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">What payment methods do you accept?</h3>
            <p className="text-gray-600 text-sm">
              We accept all major credit cards, bank transfers, and PayPal. Enterprise 
              customers can also pay via invoice.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}