#!/usr/bin/env perl
use strict;
use warnings;
use LWP::UserAgent;
use JSON::XS;
use Math::BigFloat;

package Web3Client;

sub new {
    my ($class, $rpc_url) = @_;
    $rpc_url //= 'https://eth.llamarpc.com';

    my $self = {
        rpc_url => $rpc_url,
        request_id => 0,
        ua => LWP::UserAgent->new(timeout => 30),
        json => JSON::XS->new->utf8
    };

    return bless $self, $class;
}

sub rpc_call {
    my ($self, $method, @params) = @_;

    $self->{request_id}++;

    my $payload = {
        jsonrpc => '2.0',
        method => $method,
        params => \@params,
        id => $self->{request_id}
    };

    my $response = $self->{ua}->post(
        $self->{rpc_url},
        'Content-Type' => 'application/json',
        Content => $self->{json}->encode($payload)
    );

    die "HTTP error: " . $response->status_line unless $response->is_success;

    my $result = $self->{json}->decode($response->content);
    die "RPC error: " . $result->{error}{message} if $result->{error};

    return $result->{result};
}

sub hex_to_int {
    my ($self, $hex) = @_;
    $hex =~ s/^0x//;
    return Math::BigFloat->new("0x$hex")->as_int();
}

sub wei_to_ether {
    my ($self, $wei) = @_;
    return Math::BigFloat->new($wei)->bdiv('1e18');
}

sub wei_to_gwei {
    my ($self, $wei) = @_;
    return Math::BigFloat->new($wei)->bdiv('1e9');
}

sub get_block_number {
    my ($self) = @_;
    my $result = $self->rpc_call('eth_blockNumber');
    return $self->hex_to_int($result);
}

sub get_balance {
    my ($self, $address) = @_;
    my $result = $self->rpc_call('eth_getBalance', $address, 'latest');
    my $wei = $self->hex_to_int($result);
    return $self->wei_to_ether($wei);
}

sub get_gas_price {
    my ($self) = @_;
    my $result = $self->rpc_call('eth_gasPrice');
    my $wei = $self->hex_to_int($result);
    return $self->wei_to_gwei($wei);
}

# Example usage
package main;

if ($0 eq __FILE__) {
    print "🔮 Perl Web3 Client\n";
    print "-" x 40 . "\n";

    my $client = Web3Client->new();

    my $block = $client->get_block_number();
    print "📦 Block Number: $block\n";

    my $gas = $client->get_gas_price();
    printf "⛽ Gas Price: %.2f Gwei\n", $gas;

    my $address = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045';
    my $balance = $client->get_balance($address);
    printf "💰 Balance: %.4f ETH\n", $balance;
}

1;
