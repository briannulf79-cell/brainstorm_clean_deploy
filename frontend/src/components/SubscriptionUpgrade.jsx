import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Check, Crown, Zap, TrendingUp, AlertTriangle, CreditCard } from 'lucide-react'

const PLANS = [
  {
    id: 'starter',
    name: 'Starter',
    price: 97,
    yearlyPrice: 970,
    description: 'Perfect for small businesses getting started',
    features: [
      'Up to 1,000 contacts',
      'Basic CRM features',
      'Email campaigns',
      'Basic analytics',
      '5 websites',
      'Standard support'
    ],
    popular: false
  },
  {
    id: 'professional',
    name: 'Professional',
    price: 297,
    yearlyPrice: 2970,
    description: 'Ideal for growing businesses and agencies',
    features: [
      'Up to 10,000 contacts',
      'Advanced CRM & automation',
      'AI-powered lead scoring',
      'Advanced analytics',
      'Unlimited websites',
      'SMS campaigns',
      'Priority support',
      'White-label options'
    ],
    popular: true
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 497,
    yearlyPrice: 4970,
    description: 'For large organizations with advanced needs',
    features: [
      'Unlimited contacts',
      'Full AI suite',
      'Predictive analytics',
      'Custom integrations',
      'Unlimited everything',
      'Dedicated account manager',
      '24/7 phone support',
      'Custom training'
    ],
    popular: false
  },
  {
    id: 'agency',
    name: 'Agency',
    price: 997,
    yearlyPrice: 9970,
    description: 'Complete white-label solution for agencies',
    features: [
      'Everything in Enterprise',
      'Full white-label branding',
      'Reseller program access',
      'Client management tools',
      'Revenue sharing',
      'Custom domain setup',
      'Agency training program',
      'Marketing materials'
    ],
    popular: false
  }
]

export default function SubscriptionUpgrade({ user, onUpgrade, onClose }) {
  const [selectedPlan, setSelectedPlan] = useState('professional')
  const [billingCycle, setBillingCycle] = useState('monthly')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleUpgrade = async () => {
    setLoading(true)
    setError('')

    try {
      const API_URL = import.meta.env.VITE_API_URL || ''
      const token = localStorage.getItem('authToken')
      
      const response = await fetch(`${API_URL}/api/subscription/upgrade`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          plan: selectedPlan,
          billing_cycle: billingCycle
        })
      })

      const data = await response.json()

      if (response.ok) {
        onUpgrade(data.user, data.subscription)
      } else {
        setError(data.error || 'Upgrade failed')
      }
    } catch (error) {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const selectedPlanData = PLANS.find(p => p.id === selectedPlan)
  const price = billingCycle === 'yearly' ? selectedPlanData.yearlyPrice : selectedPlanData.price
  const savings = billingCycle === 'yearly' ? Math.round((selectedPlanData.price * 12 - selectedPlanData.yearlyPrice) / (selectedPlanData.price * 12) * 100) : 0

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-6xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center text-2xl">
            <Crown className="h-6 w-6 mr-2 text-yellow-500" />
            Upgrade Your Subscription
          </DialogTitle>
          <DialogDescription>
            {user?.is_trial_expired 
              ? `Your trial has expired. Choose a plan to continue using Brainstorm AI Kit.`
              : `You have ${user?.days_remaining || 0} days left in your trial. Upgrade now to unlock all features.`
            }
          </DialogDescription>
        </DialogHeader>

        {user?.is_trial_expired && (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              Your trial has expired. Please upgrade to continue accessing your account.
            </AlertDescription>
          </Alert>
        )}

        {/* Billing Toggle */}
        <div className="flex justify-center mb-6">
          <div className="bg-gray-100 p-1 rounded-lg flex">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                billingCycle === 'monthly'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                billingCycle === 'yearly'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Yearly
              <Badge variant="secondary" className="ml-2 text-xs">
                Save 20%
              </Badge>
            </button>
          </div>
        </div>

        {/* Plans Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {PLANS.map((plan) => {
            const planPrice = billingCycle === 'yearly' ? plan.yearlyPrice : plan.price
            const isSelected = selectedPlan === plan.id
            
            return (
              <Card 
                key={plan.id}
                className={`cursor-pointer transition-all ${
                  isSelected 
                    ? 'ring-2 ring-blue-500 shadow-lg' 
                    : 'hover:shadow-md'
                } ${plan.popular ? 'border-blue-500' : ''}`}
                onClick={() => setSelectedPlan(plan.id)}
              >
                <CardHeader className="text-center pb-2">
                  {plan.popular && (
                    <Badge className="w-fit mx-auto mb-2 bg-blue-500">
                      Most Popular
                    </Badge>
                  )}
                  <CardTitle className="text-lg">{plan.name}</CardTitle>
                  <div className="text-3xl font-bold">
                    ${billingCycle === 'yearly' ? Math.round(planPrice / 12) : planPrice}
                    <span className="text-sm font-normal text-gray-600">
                      /{billingCycle === 'yearly' ? 'mo' : 'month'}
                    </span>
                  </div>
                  {billingCycle === 'yearly' && (
                    <div className="text-sm text-gray-600">
                      ${planPrice} billed annually
                    </div>
                  )}
                  <CardDescription className="text-xs">
                    {plan.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent className="pt-2">
                  <ul className="space-y-2 text-sm">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="flex items-start">
                        <Check className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Selected Plan Summary */}
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-lg">
                  {selectedPlanData.name} Plan
                </h3>
                <p className="text-gray-600">
                  {billingCycle === 'yearly' ? 'Annual' : 'Monthly'} billing
                  {savings > 0 && (
                    <Badge variant="secondary" className="ml-2">
                      Save {savings}%
                    </Badge>
                  )}
                </p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold">
                  ${billingCycle === 'yearly' ? Math.round(price / 12) : price}/mo
                </div>
                {billingCycle === 'yearly' && (
                  <div className="text-sm text-gray-600">
                    ${price} billed annually
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {error && (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Action Buttons */}
        <div className="flex justify-end space-x-3 pt-4 border-t">
          {!user?.is_trial_expired && (
            <Button variant="outline" onClick={onClose}>
              Continue Trial
            </Button>
          )}
          <Button 
            onClick={handleUpgrade}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700"
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Processing...
              </div>
            ) : (
              <>
                <CreditCard className="h-4 w-4 mr-2" />
                Upgrade to {selectedPlanData.name}
              </>
            )}
          </Button>
        </div>

        {/* Trust Indicators */}
        <div className="text-center text-sm text-gray-600 pt-4 border-t">
          <div className="flex items-center justify-center space-x-4">
            <div className="flex items-center">
              <Zap className="h-4 w-4 mr-1 text-green-500" />
              Instant activation
            </div>
            <div className="flex items-center">
              <TrendingUp className="h-4 w-4 mr-1 text-blue-500" />
              Cancel anytime
            </div>
            <div className="flex items-center">
              <Check className="h-4 w-4 mr-1 text-green-500" />
              30-day money back
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

