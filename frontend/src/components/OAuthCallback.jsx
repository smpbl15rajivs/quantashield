import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Shield, CheckCircle, XCircle, Loader2 } from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'

const OAuthCallback = ({ onLogin }) => {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [status, setStatus] = useState('processing') // 'processing', 'success', 'error'
  const [message, setMessage] = useState('')
  const [userInfo, setUserInfo] = useState(null)

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Get parameters from URL
        const token = searchParams.get('token')
        const error = searchParams.get('error')
        const errorDescription = searchParams.get('error_description')

        if (error) {
          setStatus('error')
          const errorMsg = errorDescription || error
          setMessage(`Authentication failed: ${errorMsg}`)
          
          // Log error for debugging (remove in production)
          console.error('OAuth Error:', { error, errorDescription })
          return
        }

        if (!token) {
          setStatus('error')
          setMessage('No authentication token received. Please try again.')
          return
        }

        // Validate token format (basic check)
        const tokenParts = token.split('.')
        if (tokenParts.length !== 3) {
          setStatus('error')
          setMessage('Invalid authentication token format.')
          return
        }

        // Decode and validate token
        try {
          const payload = JSON.parse(atob(tokenParts[1]))
          
          // Check token expiration
          if (payload.exp && payload.exp < Date.now() / 1000) {
            setStatus('error')
            setMessage('Authentication token has expired. Please try again.')
            return
          }

          // Validate required fields
          if (!payload.username || !payload.email) {
            setStatus('error')
            setMessage('Incomplete user information received.')
            return
          }
          
          setUserInfo({
            username: payload.username,
            email: payload.email,
            provider: payload.provider || 'federated',
            isAuthenticated: true,
            token: token
          })
          
          setStatus('success')
          setMessage('Successfully authenticated! Redirecting to dashboard...')
          
          // Store token securely
          localStorage.setItem('authToken', token)
          localStorage.setItem('userInfo', JSON.stringify({
            username: payload.username,
            email: payload.email,
            provider: payload.provider || 'federated'
          }))
          
          // Redirect to dashboard after 2 seconds
          setTimeout(() => {
            onLogin && onLogin({
              username: payload.username,
              email: payload.email,
              provider: payload.provider || 'federated',
              isAuthenticated: true,
              token: token
            })
          }, 2000)
          
        } catch (tokenError) {
          console.error('Token parsing error:', tokenError)
          setStatus('error')
          setMessage('Invalid authentication token. Please try again.')
        }

      } catch (err) {
        console.error('OAuth callback error:', err)
        setStatus('error')
        setMessage('Authentication processing failed. Please try again.')
      }
    }

    handleCallback()
  }, [searchParams, onLogin])

  const handleRetry = () => {
    navigate('/')
  }

  const renderProcessing = () => (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="flex justify-center mb-4">
          <div className="p-3 bg-blue-100 rounded-full">
            <Loader2 className="h-8 w-8 text-blue-600 animate-spin" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold">Processing Authentication</CardTitle>
        <CardDescription>
          Please wait while we complete your login...
        </CardDescription>
      </CardHeader>
      <CardContent className="text-center">
        <div className="space-y-4">
          <div className="animate-pulse">
            <div className="h-2 bg-blue-200 rounded-full w-3/4 mx-auto mb-2"></div>
            <div className="h-2 bg-blue-200 rounded-full w-1/2 mx-auto"></div>
          </div>
          <p className="text-sm text-gray-600">
            Verifying your credentials with the identity provider...
          </p>
        </div>
      </CardContent>
    </Card>
  )

  const renderSuccess = () => (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="flex justify-center mb-4">
          <div className="p-3 bg-green-100 rounded-full">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold text-green-600">Authentication Successful!</CardTitle>
        <CardDescription>
          Welcome to QuantaShield
        </CardDescription>
      </CardHeader>
      <CardContent className="text-center space-y-4">
        {userInfo && (
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-sm text-green-800">
              <strong>Welcome, {userInfo.username}!</strong>
            </p>
            {userInfo.email && (
              <p className="text-xs text-green-600 mt-1">
                {userInfo.email}
              </p>
            )}
          </div>
        )}
        
        <Alert>
          <CheckCircle className="h-4 w-4" />
          <AlertDescription>
            {message}
          </AlertDescription>
        </Alert>

        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto"></div>
      </CardContent>
    </Card>
  )

  const renderError = () => (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="flex justify-center mb-4">
          <div className="p-3 bg-red-100 rounded-full">
            <XCircle className="h-8 w-8 text-red-600" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold text-red-600">Authentication Failed</CardTitle>
        <CardDescription>
          There was a problem with your login
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Alert variant="destructive">
          <XCircle className="h-4 w-4" />
          <AlertDescription>
            {message}
          </AlertDescription>
        </Alert>

        <Button onClick={handleRetry} className="w-full">
          Try Again
        </Button>

        <div className="text-center text-sm text-gray-600">
          <p>If the problem persists, please contact support.</p>
        </div>
      </CardContent>
    </Card>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="flex items-center justify-center mb-4">
            <Shield className="h-12 w-12 text-blue-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            QuantaShield
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Enterprise Cybersecurity Platform
          </p>
        </div>

        {/* Status Content */}
        {status === 'processing' && renderProcessing()}
        {status === 'success' && renderSuccess()}
        {status === 'error' && renderError()}

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>© 2024 QuantaShield. All rights reserved.</p>
          <p className="mt-1">Powered by AI/ML threat detection</p>
        </div>
      </div>
    </div>
  )
}

export default OAuthCallback

