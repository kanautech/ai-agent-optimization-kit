# Zenn 記事の公開手順（GitHub連携方式）

Zennは、GitHubリポジトリと連携して記事を管理・自動公開する公式の仕組みを提供しています。以下の手順に従って、作成した `ZENN_ARTICLE.md` をZennに公開します。

## 1. Zenn CLI のセットアップとリポジトリ初期化
Zennの記事管理用リポジトリ（または既存のプロジェクト）で、Zenn CLIをインストールして初期化します。

```bash
# Zenn CLI のインストール
npm install zenn-cli --save-dev

# 記事用ディレクトリの作成
npx zenn init
```

## 2. 記事ファイルの配置
作成された `articles/` ディレクトリ内に、今回執筆した `ZENN_ARTICLE.md` を配置します（ファイル名はスラッグ名を含んだ形式、例: `ai-tdd-optimization-kit.md`）。

## 3. GitHubリポジトリへのプッシュ
Zennと連携しているGitHubリポジトリの `main`（または `master`）ブランチにコードをプッシュします。

```bash
git add articles/ai-tdd-optimization-kit.md
git commit -m "Add Zenn technical article on AI-Driven TDD Optimization"
git push origin master
```

## 4. Zennダッシュボードでの確認
Zennの公式サイトにログインし、GitHub連携設定が有効な状態でWebhooksまたは自動同期により、記事がプレビュー・公開されます。
