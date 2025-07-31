import { useState } from 'react'
import { 
  Shield, 
  Eye, 
  EyeOff, 
  Lock, 
  User, 
  Smartphone,
  KeyRound,
  AlertCircle
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'

const LoginPage = ({ onLogin }) => {
  const [step, setStep] = useState('credentials') // 'credentials', '2fa', 'success'
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  })
  
  const [twoFactorCode, setTwoFactorCode] = useState('')

  const handleSocialLogin = async (provider) => {
    setLoading(true)
    setError('')

    try {
      // Get OAuth providers list first to verify backend is available
      const providersResponse = await fetch('https://xlhyimc39vgm.manus.space/api/auth/providers')
      if (!providersResponse.ok) {
        throw new Error('OAuth service unavailable')
      }

      // Initiate OAuth login by redirecting to backend
      const redirectUrl = encodeURIComponent(`http://quantashield.in/auth/callback`)
      const loginUrl = `https://xlhyimc39vgm.manus.space/api/auth/${provider}/login?redirect_url=${redirectUrl}`
      
      // Redirect to OAuth provider
      window.location.href = loginUrl
    } catch (err) {
      setError(`Failed to login with ${provider}. Please try again.`)
      setLoading(false)
    }
  }

  const handleCredentialsSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Simulate API call
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Validate credentials (demo purposes)
      if (credentials.username === 'admin' && credentials.password === 'password') {
        setStep('2fa')
      } else {
        setError('Invalid username or password')
      }
    } catch (err) {
      setError('Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handle2FASubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Validate 2FA code (demo purposes)
      if (twoFactorCode === '123456') {
        setStep('success')
        setTimeout(() => {
          onLogin && onLogin()
        }, 1500)
      } else {
        setError('Invalid 2FA code')
      }
    } catch (err) {
      setError('2FA verification failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const renderCredentialsStep = () => (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="flex justify-center mb-4">
          <div className="p-3 bg-blue-100 rounded-full">
            <Shield className="h-8 w-8 text-blue-600" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold">Welcome to QuantaShield</CardTitle>
        <CardDescription>
          Sign in to your cybersecurity dashboard
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Social Login Section */}
        <div className="space-y-3 mb-6">
          <div className="text-center text-sm text-gray-600 mb-4">
            Sign in with your preferred account
          </div>
          
          {/* Social Login Buttons */}
          <Button
            onClick={() => handleSocialLogin('google')}
            variant="outline"
            className="w-full justify-start hover:bg-red-50 border-gray-200 hover:border-red-300 transition-all duration-200"
            disabled={loading}
          >
            <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Continue with Google
          </Button>

          <Button
            onClick={() => handleSocialLogin('microsoft')}
            variant="outline"
            className="w-full justify-start hover:bg-blue-50 border-gray-200 hover:border-blue-300 transition-all duration-200"
            disabled={loading}
          >
            <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
              <path fill="#F25022" d="M1 1h10v10H1z"/>
              <path fill="#00A4EF" d="M13 1h10v10H13z"/>
              <path fill="#7FBA00" d="M1 13h10v10H1z"/>
              <path fill="#FFB900" d="M13 13h10v10H13z"/>
            </svg>
            Continue with Microsoft
          </Button>

          <Button
            onClick={() => handleSocialLogin('facebook')}
            variant="outline"
            className="w-full justify-start hover:bg-blue-50 border-gray-200 hover:border-blue-600 transition-all duration-200"
            disabled={loading}
          >
            <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
              <path fill="#1877F2" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
            Continue with Facebook
          </Button>

          <Button
            onClick={() => handleSocialLogin('linkedin')}
            variant="outline"
            className="w-full justify-start hover:bg-blue-50 border-gray-200 hover:border-blue-700 transition-all duration-200"
            disabled={loading}
          >
            <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
              <path fill="#0077B5" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
            Continue with LinkedIn
          </Button>

          <Button
            onClick={() => handleSocialLogin('twitter')}
            variant="outline"
            className="w-full justify-start hover:bg-sky-50 border-gray-200 hover:border-sky-500 transition-all duration-200"
            disabled={loading}
          >
            <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
              <path fill="#1DA1F2" d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
            </svg>
            Continue with Twitter
          </Button>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t border-gray-300" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white px-2 text-gray-500">Or continue with</span>
            </div>
          </div>
        </div>

        <form onSubmit={handleCredentialsSubmit} className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          
          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                id="username"
                type="text"
                placeholder="Enter your username"
                value={credentials.username}
                onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                className="pl-10"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                value={credentials.password}
                onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                className="pl-10 pr-10"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Demo credentials: admin / password
          </p>
        </div>
      </CardContent>
    </Card>
  )

  const render2FAStep = () => (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="flex justify-center mb-4">
          <div className="p-3 bg-green-100 rounded-full">
            <Smartphone className="h-8 w-8 text-green-600" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold">Two-Factor Authentication</CardTitle>
        <CardDescription>
          Enter the 6-digit code from your authenticator app
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handle2FASubmit} className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            <Label htmlFor="twoFactorCode">Authentication Code</Label>
            <div className="relative">
              <KeyRound className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                id="twoFactorCode"
                type="text"
                placeholder="000000"
                value={twoFactorCode}
                onChange={(e) => setTwoFactorCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                className="pl-10 text-center text-lg tracking-widest"
                maxLength={6}
                required
              />
            </div>
          </div>

          <Button type="submit" className="w-full" disabled={loading || twoFactorCode.length !== 6}>
            {loading ? 'Verifying...' : 'Verify Code'}
          </Button>

          <Button 
            type="button" 
            variant="outline" 
            className="w-full"
            onClick={() => setStep('credentials')}
          >
            Back to Login
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Demo 2FA code: 123456
          </p>
        </div>
      </CardContent>
    </Card>
  )

  const renderSuccessStep = () => (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="text-center">
        <div className="flex justify-center mb-4">
          <div className="p-3 bg-green-100 rounded-full animate-pulse">
            <Shield className="h-8 w-8 text-green-600" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold text-green-600">Login Successful!</CardTitle>
        <CardDescription>
          Redirecting to your dashboard...
        </CardDescription>
      </CardHeader>
      <CardContent className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto"></div>
      </CardContent>
    </Card>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Security Features Banner */}
        <div className="mb-8 text-center">
          <div className="flex justify-center space-x-4 mb-4">
            <Badge variant="outline" className="bg-white/80">
              <Lock className="w-3 h-3 mr-1" />
              End-to-End Encryption
            </Badge>
            <Badge variant="outline" className="bg-white/80">
              <Shield className="w-3 h-3 mr-1" />
              Multi-Factor Auth
            </Badge>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            QuantaShield
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Enterprise Cybersecurity Platform
          </p>
        </div>

        {/* Login Steps */}
        {step === 'credentials' && renderCredentialsStep()}
        {step === '2fa' && render2FAStep()}
        {step === 'success' && renderSuccessStep()}

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>© 2024 QuantaShield. All rights reserved.</p>
          <p className="mt-1">Powered by AI/ML threat detection</p>
        </div>
      </div>
    </div>
  )
}

export default LoginPage

