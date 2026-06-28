/**
 * ロット一覧画面 Alpine.js コンポーネント
 */
function lotsPage() {
  return {
    // トースト状態
    toastVisible: false,
    toastMsg: "",
    _toastTimer: null,

    init() {
      // URL パラメータのトーストメッセージを発火
      const params = new URLSearchParams(window.location.search);
      const msg = window.__toastMsg;
      if (msg) {
        this.$nextTick(() => this.showToast(msg));
      }

      // Alpine の MutationObserver が HTMX 差し込み後の x-data を自動検知する
      // lotDialog 関数はメインページで事前ロード済みのため初期化競合は発生しない
    },

    showToast(msg) {
      this.toastMsg = msg;
      this.toastVisible = true;
      clearTimeout(this._toastTimer);
      this._toastTimer = setTimeout(() => {
        this.toastVisible = false;
      }, 2600);
    },
  };
}
