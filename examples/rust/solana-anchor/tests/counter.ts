import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Counter } from "../target/types/counter";
import { expect } from "chai";

describe("counter", () => {
  // Configure the client to use the local cluster
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.Counter as Program<Counter>;
  const counterAccount = anchor.web3.Keypair.generate();

  it("Initializes the counter", async () => {
    await program.methods
      .initialize()
      .accounts({
        counter: counterAccount.publicKey,
        user: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([counterAccount])
      .rpc();

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

    expect(account.count.toNumber()).to.equal(0);
    expect(account.authority.toString()).to.equal(
      provider.wallet.publicKey.toString()
    );
  });

  it("Increments the counter", async () => {
    await program.methods
      .increment()
      .accounts({
        counter: counterAccount.publicKey,
        authority: provider.wallet.publicKey,
      })
      .rpc();

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

    expect(account.count.toNumber()).to.equal(1);
  });

  it("Increments the counter again", async () => {
    await program.methods
      .increment()
      .accounts({
        counter: counterAccount.publicKey,
        authority: provider.wallet.publicKey,
      })
      .rpc();

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

    expect(account.count.toNumber()).to.equal(2);
  });

  it("Decrements the counter", async () => {
    await program.methods
      .decrement()
      .accounts({
        counter: counterAccount.publicKey,
        authority: provider.wallet.publicKey,
      })
      .rpc();

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

    expect(account.count.toNumber()).to.equal(1);
  });

  it("Sets the counter to a specific value", async () => {
    await program.methods
      .set(new anchor.BN(42))
      .accounts({
        counter: counterAccount.publicKey,
        authority: provider.wallet.publicKey,
      })
      .rpc();

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

    expect(account.count.toNumber()).to.equal(42);
  });

  it("Resets the counter", async () => {
    await program.methods
      .reset()
      .accounts({
        counter: counterAccount.publicKey,
        authority: provider.wallet.publicKey,
      })
      .rpc();

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

    expect(account.count.toNumber()).to.equal(0);
  });

  it("Transfers authority", async () => {
    const newAuthority = anchor.web3.Keypair.generate();

    await program.methods
      .transferAuthority(newAuthority.publicKey)
      .accounts({
        counter: counterAccount.publicKey,
        authority: provider.wallet.publicKey,
      })
      .rpc();

    const account = await program.account.counter.fetch(
      counterAccount.publicKey
    );

    expect(account.authority.toString()).to.equal(
      newAuthority.publicKey.toString()
    );
  });

  it("Fails when non-authority tries to increment", async () => {
    const unauthorizedUser = anchor.web3.Keypair.generate();

    try {
      await program.methods
        .increment()
        .accounts({
          counter: counterAccount.publicKey,
          authority: unauthorizedUser.publicKey,
        })
        .signers([unauthorizedUser])
        .rpc();

      expect.fail("Expected error was not thrown");
    } catch (error) {
      expect(error.toString()).to.include("Unauthorized");
    }
  });
});
