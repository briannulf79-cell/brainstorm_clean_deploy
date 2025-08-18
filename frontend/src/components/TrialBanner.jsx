import { useState } from 'react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Crown, Clock, X } from 'lucide-react'

export default function TrialBanner({ user, onUpgrade, onDismiss }) {
  const [dismissed, setDismissed] = useState(false)

  if (dismissed || !user || user.subscription_status !== 'trial') {
    return null
  }

  const daysRemaining = user.days_remaining || 0
  const isExpiringSoon = daysRemaining <= 7
  const isExpired = user.is_trial_expired

  if (isExpired) {
    return (
      <Alert variant="destructive" className="mb-4">
        <Crown className="h-4 w-4" />
        <AlertDescription className="flex items-center justify-between">
          <span>
            <strong>Trial Expired!</strong> Your trial has ended. Upgrade now to continue using Brainstorm AI Kit.
          </span>
          <Button 
            size="sm" 
            onClick={onUpgrade}
            className="ml-4"
          >
            Upgrade Now
          </Button>
        </AlertDescription>
      </Alert>
    )
  }

  return (
    <Alert className={`mb-4 ${isExpiringSoon ? 'border-orange-200 bg-orange-50' : 'border-blue-200 bg-blue-50'}`}>
      <Clock className={`h-4 w-4 ${isExpiringSoon ? 'text-orange-600' : 'text-blue-600'}`} />
      <AlertDescription className="flex items-center justify-between">
        <span className={isExpiringSoon ? 'text-orange-800' : 'text-blue-800'}>
          <strong>Trial Active:</strong> {daysRemaining} day{daysRemaining !== 1 ? 's' : ''} remaining. 
          {isExpiringSoon && ' Upgrade soon to avoid interruption!'}
        </span>
        <div className="flex items-center space-x-2">
          <Button 
            size="sm" 
            onClick={onUpgrade}
            className={isExpiringSoon ? 'bg-orange-600 hover:bg-orange-700' : 'bg-blue-600 hover:bg-blue-700'}
          >
            <Crown className="h-3 w-3 mr-1" />
            Upgrade
          </Button>
          <Button 
            size="sm" 
            variant="ghost" 
            onClick={() => setDismissed(true)}
            className="p-1"
          >
            <X className="h-3 w-3" />
          </Button>
        </div>
      </AlertDescription>
    </Alert>
  )
}

