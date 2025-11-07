use anchor_lang::prelude::*;

declare_id!("11111111111111111111111111111111");

#[program]
pub mod counter {
    use super::*;

    /// Initialize a new counter account
    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.count = 0;
        counter.authority = ctx.accounts.user.key();
        msg!("Counter initialized with count: {}", counter.count);
        Ok(())
    }

    /// Increment the counter
    pub fn increment(ctx: Context<Update>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.count = counter.count.checked_add(1)
            .ok_or(ErrorCode::Overflow)?;
        msg!("Counter incremented to: {}", counter.count);
        Ok(())
    }

    /// Decrement the counter
    pub fn decrement(ctx: Context<Update>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.count = counter.count.checked_sub(1)
            .ok_or(ErrorCode::Underflow)?;
        msg!("Counter decremented to: {}", counter.count);
        Ok(())
    }

    /// Set counter to a specific value (authority only)
    pub fn set(ctx: Context<Update>, new_count: u64) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.count = new_count;
        msg!("Counter set to: {}", counter.count);
        Ok(())
    }

    /// Reset counter to zero (authority only)
    pub fn reset(ctx: Context<Update>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.count = 0;
        msg!("Counter reset to: {}", counter.count);
        Ok(())
    }

    /// Transfer authority to a new user
    pub fn transfer_authority(
        ctx: Context<TransferAuthority>,
        new_authority: Pubkey,
    ) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.authority = new_authority;
        msg!("Authority transferred to: {}", new_authority);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = user,
        space = 8 + Counter::INIT_SPACE
    )]
    pub counter: Account<'info, Counter>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Update<'info> {
    #[account(
        mut,
        has_one = authority @ ErrorCode::Unauthorized
    )]
    pub counter: Account<'info, Counter>,
    pub authority: Signer<'info>,
}

#[derive(Accounts)]
pub struct TransferAuthority<'info> {
    #[account(
        mut,
        has_one = authority @ ErrorCode::Unauthorized
    )]
    pub counter: Account<'info, Counter>,
    pub authority: Signer<'info>,
}

#[account]
#[derive(InitSpace)]
pub struct Counter {
    pub count: u64,
    pub authority: Pubkey,
}

#[error_code]
pub enum ErrorCode {
    #[msg("Arithmetic overflow occurred")]
    Overflow,
    #[msg("Arithmetic underflow occurred")]
    Underflow,
    #[msg("Unauthorized: Only the authority can perform this action")]
    Unauthorized,
}
