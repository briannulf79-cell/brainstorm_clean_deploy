import React, { useState } from 'react';
import { Check, Star, Zap, Crown, Rocket } from 'lucide-react';

const PricingPage = () => {
  const [billingCycle, setBillingCycle] = useState('monthly');
  const [selectedPlan, setSelectedPlan] = useState(null);

  const plans = [
    {
      id: 'starter',
      name: 'Starter',
      icon: <Zap className="h-8 w-8" />,
      description: 'Perfect for small businesses getting started',
      monthlyPrice: 97,
      yearlyPrice: 970,
      savings: 194,
      features: [
        'Up to 1,000 contacts',
        'Basic CRM functionality',
        'Email marketing campaigns',
        'Basic automation workflows',
        'Standard analytics dashboard',
        'Email support',
        '2 team members',
        'Basic AI lead scoring'
      ],
      limitations: [
        'Limited to 5 active campaigns',
        'Basic reporting only',
        'No advanced AI features'
      ],
      popular: false,
      color: 'blue'
    },
    {
      id: 'professional',
      name: 'Professional',
      icon: <Star className="h-8 w-8" />,
      description: 'Most popular for growing businesses',
      monthlyPrice: 297,
      yearlyPrice: 2970,
      savings: 594,
      features: [
        'Up to 10,000 contacts',
        'Advanced CRM with custom fields',
        'Unlimited email & SMS campaigns',
        'Advanced automation workflows',
        'AI-powered analytics dashboard',
        'Priority email & chat support',
        '10 team members',
        'Advanced AI lead scoring',
        'Predictive analytics',
        'Conversation sentiment analysis',
        'Custom integrations',
        'White-label options'
      ],
      limitations: [],
      popular: true,
      color: 'purple'
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      icon: <Crown className="h-8 w-8" />,
      description: 'For large organizations with advanced needs',
      monthlyPrice: 497,
      yearlyPrice: 4970,
      savings: 994,
      features: [
        'Unlimited contacts',
        'Enterprise CRM with custom objects',
        'Unlimited everything',
        'Advanced AI automation workflows',
        'Enterprise analytics & reporting',
        'Dedicated account manager',
        'Unlimited team members',
        'Full AI suite with custom models',
        'Advanced predictive analytics',
        'Revenue forecasting',
        'Custom AI training',
        'Full white-label platform',
        'API access & webhooks',
        'Custom integrations',
        'Priority phone support',
        'SLA guarantee'
      ],
      limitations: [],
      popular: false,
      color: 'gold'
    },
    {
      id: 'agency',
      name: 'Agency',
      icon: <Rocket className="h-8 w-8" />,
      description: 'For agencies managing multiple clients',
      monthlyPrice: 997,
      yearlyPrice: 9970,
      savings: 1994,
      features: [
        'Everything in Enterprise',
        'Unlimited client accounts',
        'Multi-tenant architecture',
        'Agency dashboard',
        'Client billing management',
        'Revenue sharing options',
        'Custom branding per client',
        'Agency-specific AI models',
        'Advanced client reporting',
        'Reseller program access',
        'Training & certification',
        'Marketing materials provided',
        'Dedicated success manager'
      ],
      limitations: [],
      popular: false,
      color: 'green'
    }
  ];

  const getColorClasses = (color, isSelected = false) => {
    const colors = {
      blue: {
        bg: isSelected ? 'bg-blue-50' : 'bg-white',
        border: isSelected ? 'border-blue-500' : 'border-gray-200',
        button: 'bg-blue-600 hover:bg-blue-700',
        text: 'text-blue-600',
        icon: 'text-blue-600'
      },
      purple: {
        bg: isSelected ? 'bg-purple-50' : 'bg-white',
        border: isSelected ? 'border-purple-500' : 'border-gray-200',
        button: 'bg-purple-600 hover:bg-purple-700',
        text: 'text-purple-600',
        icon: 'text-purple-600'
      },
      gold: {
        bg: isSelected ? 'bg-yellow-50' : 'bg-white',
        border: isSelected ? 'border-yellow-500' : 'border-gray-200',
        button: 'bg-yellow-600 hover:bg-yellow-700',
        text: 'text-yellow-600',
        icon: 'text-yellow-600'
      },
      green: {
        bg: isSelected ? 'bg-green-50' : 'bg-white',
        border: isSelected ? 'border-green-500' : 'border-gray-200',
        button: 'bg-green-600 hover:bg-green-700',
        text: 'text-green-600',
        icon: 'text-green-600'
      }
    };
    return colors[color];
  };

  const handleSelectPlan = (planId) => {
    setSelectedPlan(planId);
    // Here you would typically redirect to payment processing
    console.log('Selected plan:', planId);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Brainstorm AI Kit Plan
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Powerful AI-driven CRM and marketing automation for every business size
          </p>
          
          {/* Billing Toggle */}
          <div className="flex items-center justify-center mb-8">
            <span className={`mr-3 ${billingCycle === 'monthly' ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              Monthly
            </span>
            <button
              onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'yearly' : 'monthly')}
              className="relative inline-flex h-6 w-11 items-center rounded-full bg-blue-600 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  billingCycle === 'yearly' ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
            <span className={`ml-3 ${billingCycle === 'yearly' ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              Yearly
            </span>
            {billingCycle === 'yearly' && (
              <span className="ml-2 bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                Save 20%
              </span>
            )}
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {plans.map((plan) => {
            const isSelected = selectedPlan === plan.id;
            const colorClasses = getColorClasses(plan.color, isSelected);
            const price = billingCycle === 'monthly' ? plan.monthlyPrice : plan.yearlyPrice;
            const originalYearlyPrice = plan.monthlyPrice * 12;
            
            return (
              <div
                key={plan.id}
                className={`relative rounded-2xl shadow-lg transition-all duration-300 hover:shadow-xl ${colorClasses.bg} ${colorClasses.border} border-2 ${
                  plan.popular ? 'ring-2 ring-purple-500 ring-opacity-50' : ''
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-purple-600 text-white px-4 py-1 rounded-full text-sm font-medium">
                      Most Popular
                    </span>
                  </div>
                )}
                
                <div className="p-8">
                  {/* Plan Header */}
                  <div className="text-center mb-6">
                    <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4 ${colorClasses.icon}`}>
                      {plan.icon}
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                    <p className="text-gray-600 text-sm">{plan.description}</p>
                  </div>

                  {/* Pricing */}
                  <div className="text-center mb-6">
                    <div className="flex items-baseline justify-center">
                      <span className="text-4xl font-bold text-gray-900">${price}</span>
                      <span className="text-gray-500 ml-1">/{billingCycle === 'monthly' ? 'mo' : 'yr'}</span>
                    </div>
                    {billingCycle === 'yearly' && (
                      <div className="mt-2">
                        <span className="text-sm text-gray-500 line-through">${originalYearlyPrice}/yr</span>
                        <span className="text-sm text-green-600 ml-2 font-medium">
                          Save ${plan.savings}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Features */}
                  <div className="mb-8">
                    <ul className="space-y-3">
                      {plan.features.map((feature, index) => (
                        <li key={index} className="flex items-start">
                          <Check className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-700 text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* CTA Button */}
                  <button
                    onClick={() => handleSelectPlan(plan.id)}
                    className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-colors ${colorClasses.button}`}
                  >
                    {isSelected ? 'Selected' : 'Get Started'}
                  </button>
                  
                  <p className="text-center text-xs text-gray-500 mt-3">
                    14-day free trial • No credit card required
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Features Comparison */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Compare All Features
          </h2>
          
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-900">Features</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-900">Starter</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-900">Professional</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-900">Enterprise</th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-900">Agency</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Contacts</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">1,000</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">10,000</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Unlimited</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Unlimited</td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-900">Team Members</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">2</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">10</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Unlimited</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Unlimited</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">AI Lead Scoring</td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-900">Predictive Analytics</td>
                    <td className="px-6 py-4 text-center text-gray-400">—</td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">White-label Options</td>
                    <td className="px-6 py-4 text-center text-gray-400">—</td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-900">API Access</td>
                    <td className="px-6 py-4 text-center text-gray-400">—</td>
                    <td className="px-6 py-4 text-center text-gray-400">—</td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                    <td className="px-6 py-4 text-center"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Frequently Asked Questions
          </h2>
          
          <div className="max-w-3xl mx-auto space-y-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Can I change my plan later?
              </h3>
              <p className="text-gray-600">
                Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately, and we'll prorate any billing differences.
              </p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Is there a free trial?
              </h3>
              <p className="text-gray-600">
                Yes, all plans come with a 14-day free trial. No credit card required to start your trial.
              </p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                What makes Brainstorm AI Kit different from Go High Level?
              </h3>
              <p className="text-gray-600">
                Our platform features advanced AI integration throughout, superior user experience, predictive analytics, and enterprise-grade features at competitive pricing.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <div className="bg-blue-600 rounded-2xl p-12 text-white">
            <h2 className="text-3xl font-bold mb-4">
              Ready to Transform Your Business?
            </h2>
            <p className="text-xl mb-8 text-blue-100">
              Join thousands of businesses already using Brainstorm AI Kit to grow faster with AI-powered automation.
            </p>
            <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Start Your Free Trial
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;

