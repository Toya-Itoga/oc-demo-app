/**
 * 日報閲覧画面 Alpine.js コンポーネント
 *
 * aiSummary(full, isNew)
 *   full  … 表示するAIまとめ全文
 *   isNew … true なら保存直後としてタイピングアニメーションを再生する
 */
function aiSummary(full, isNew) {
  return {
    phase: isNew ? "loading" : "done",
    shown: isNew ? "" : full,
    _iv: null,

    init() {
      if (!isNew) return;

      // 約1.9秒ローディング → タイピング開始
      setTimeout(() => {
        this.phase = "typing";
        let i = 0;
        this._iv = setInterval(() => {
          this.shown = full.slice(0, ++i);
          if (i >= full.length) {
            clearInterval(this._iv);
            this.phase = "done";
          }
        }, 40);
      }, 1900);
    },

    destroy() {
      clearInterval(this._iv);
    },
  };
}

/**
 * 日報閲覧画面全体のコンポーネント
 * window.__toastMsg に表示するトーストメッセージを注入する（保存直後のみ）
 */
function reportShowPage() {
  return {
    toastVisible: false,
    toastMsg: "",
    _toastTimer: null,

    init() {
      const msg = window.__toastMsg;
      if (msg) {
        this.$nextTick(() => this.showToast(msg));
      }
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
