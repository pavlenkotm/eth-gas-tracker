defmodule PhoenixWeb3.MixProject do
  use Mix.Project

  def project do
    [
      app: :phoenix_web3,
      version: "1.0.0",
      elixir: "~> 1.15",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {PhoenixWeb3.Application, []}
    ]
  end

  defp deps do
    [
      {:phoenix, "~> 1.7.10"},
      {:httpoison, "~> 2.2"},
      {:jason, "~> 1.4"},
      {:decimal, "~> 2.1"},
      {:ex_abi, "~> 0.6"},
      {:ex_keccak, "~> 0.7"}
    ]
  end
end
