import { useAccount, useConnect, useDisconnect, useEnsName } from 'wagmi'

export function WalletConnect() {
  const { address, isConnected } = useAccount()
  const { data: ensName } = useEnsName({ address })
  const { connect, connectors, error, isLoading, pendingConnector } =
    useConnect()
  const { disconnect } = useDisconnect()

  if (isConnected) {
    return (
      <div className="wallet-connected">
        <h2>✅ Wallet Connected</h2>
        <p className="address">
          {ensName ? `${ensName} (${address})` : address}
        </p>
        <button onClick={() => disconnect()} className="btn btn-danger">
          Disconnect
        </button>
      </div>
    )
  }

  return (
    <div className="wallet-connect">
      <h2>Connect Your Wallet</h2>
      {connectors.map((connector) => (
        <button
          className="btn btn-primary"
          disabled={!connector.ready}
          key={connector.id}
          onClick={() => connect({ connector })}
        >
          {connector.name}
          {!connector.ready && ' (unsupported)'}
          {isLoading &&
            connector.id === pendingConnector?.id &&
            ' (connecting)'}
        </button>
      ))}

      {error && <div className="error">{error.message}</div>}
    </div>
  )
}
